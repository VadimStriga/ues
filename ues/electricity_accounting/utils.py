from datetime import date
import io
import locale

from django.db.models import Q
from django.shortcuts import get_object_or_404
from number_to_string import get_string_by_number
import xlsxwriter

from .models import (NDS,
                     Calculation,
                     ElectricityMeter,
                     ElectricityMeteringPoint,
                     Tariff,
                     InterconnectedPoints)
from counterparties.models import Counterparty
from organization.models import Organization


def get_calculation_tariff(point_id, entry_date):
    """The function for determining the cost of the tariff selected at the
    ElectricityMeteringPoint. The VAT amount is deducted from the tariffs for
    urban and rural populations, since it was originally included in the tariffs.
    """
    tariff_f = Tariff.objects.filter(begin_tariff_period__lte=entry_date,
                                end_tariff_period__gte=entry_date).first()
    if tariff_f is not None:
        tariff = tariff_f
    else:
        tariff = Tariff.objects.first()

    point = get_object_or_404(ElectricityMeteringPoint, pk=point_id)
    if point.tariff == 'urban_tariff':
        tariff1 = tariff.urban_tariff_1 - tariff.urban_tariff_1 * NDS / (100 + NDS)
        tariff2 = tariff.urban_tariff_2 - tariff.urban_tariff_2 * NDS / (100 + NDS)
        tariff3 = tariff.urban_tariff_3 - tariff.urban_tariff_3 * NDS / (100 + NDS)
        is_population = True
        return (round(tariff1, 5),
                round(tariff2, 5),
                round(tariff3, 5),
                is_population,)
    elif point.tariff == 'rural_tariff':
        tariff1 = tariff.rural_tariff_1 - tariff.rural_tariff_1 * NDS / (100 + NDS)
        tariff2 = tariff.rural_tariff_2 - tariff.rural_tariff_2 * NDS / (100 + NDS)
        tariff3 = tariff.rural_tariff_3 - tariff.rural_tariff_3 * NDS / (100 + NDS)
        is_population = True
        return (round(tariff1, 5),
                round(tariff2, 5),
                round(tariff3, 5),
                is_population,)
    elif point.tariff == 'low_voltage_tariff':
        is_population = False
        return (tariff.low_voltage_tariff,
                tariff.low_voltage_tariff,
                tariff.low_voltage_tariff,
                is_population,)
    elif point.tariff == 'medium_voltage_tariff_1':
        is_population = False
        return (tariff.medium_voltage_tariff_1,
                tariff.medium_voltage_tariff_1,
                tariff.medium_voltage_tariff_1,
                is_population,)
    elif point.tariff == 'medium_voltage_tariff_2':
        is_population = False
        return (tariff.medium_voltage_tariff_2,
                tariff.medium_voltage_tariff_2,
                tariff.medium_voltage_tariff_2,
                is_population,)
    elif point.tariff == 'high_voltage_tariff':
        is_population = False
        return (tariff.high_voltage_tariff,
                tariff.high_voltage_tariff,
                tariff.high_voltage_tariff,
                is_population,)
    elif point.tariff == 'tariff-free':
        is_population = False
        return (0, 0, 0, is_population,)


def get_calculation_result_amount(amount, deductible_amount, losses, constant_losses):
    intermediate_amount = amount - deductible_amount
    volume_losses = intermediate_amount / 100 * losses
    result_amount = round((intermediate_amount + volume_losses + constant_losses), 2)
    return round(result_amount)


def get_calculation_accrued(result_amount, tariff1, tariff2, tariff3, margin):
    """A function for calculating charges for consumed electricity.
    The formula is derived based on tariffs for rural and urban populations,
    but it is also suitable for other tariffs.
    """
    if result_amount <= 10980:
        accrued = (tariff1 + margin) * result_amount
    elif result_amount <= 14640:
        accrued = ((tariff1 + margin) * 10980) + ((tariff2 + margin) * (result_amount - 10980))
    else:
        accrued = ((tariff1 + margin) * 10980) + ((tariff2 + margin) * 3660) + ((tariff3 + margin) * (result_amount - 14640))
    return round(accrued, 2)


def get_calculation_previous_entry_date(point_id):
    calculations = Calculation.objects.filter(point=point_id)
    if len(calculations) != 0:
        previous_entry_date = calculations[0].entry_date
    else:
        meter = ElectricityMeter.objects.filter(point=point_id).filter(is_active=True)[0]
        previous_entry_date = meter.installation_date
    return previous_entry_date


def get_calculation_previous_readings(point_id, new_readings):
    calculations = Calculation.objects.filter(point=point_id)
    if len(calculations) != 0:
        previous_readings = calculations[0].readings
    else:
        previous_readings = new_readings
    return previous_readings


def get_deductible_amount(point_id, entry_date):
    deductible_amount = 0
    lower_points = InterconnectedPoints.objects.filter(head_point=point_id).select_related('lower_point')
    for point in lower_points:
        calculations = Calculation.objects.filter(point=point.lower_point, entry_date__year=entry_date.year, entry_date__month=entry_date.month)
        for calculation in calculations:
            deductible_amount += calculation.amount
    return deductible_amount


def create_xlsx_document(request, point_id, calculation_id):
    """In the xlsx document created for calculating the consumed electricity,
    all accounting points for the selected month are taken into account.
    """
    user = request.user

    if user.first_name:
        first_name = user.first_name[0] + '.'
    else:
        first_name = user.first_name

    if user.middle_name:
        middle_name = user.middle_name[0] + '.'
    else:
        middle_name = user.middle_name

    user_name = user.last_name + ' ' + first_name + middle_name

    calculation = get_object_or_404(Calculation, pk=calculation_id)
    month_m = calculation.entry_date.strftime('%m')
    point = get_object_or_404(ElectricityMeteringPoint, pk=point_id)
    counterparty = point.contract.counterparty
    counterparty_name = counterparty.short_name
    points = ElectricityMeteringPoint.objects.filter(contract=point.contract)
    calculations = Calculation.objects.filter(point__in=points).filter(entry_date__month=month_m)
    organization = Organization.objects.first()

    locale.setlocale(locale.LC_ALL, "")
    month = calculation.entry_date.strftime('%B')
    year = calculation.entry_date.strftime('%Y')
    conclusion_date = point.contract.conclusion_date.strftime('%d.%m.%Y')

    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet1 = workbook.add_worksheet('Расчет')
    title = workbook.add_format({
        'font_name':'Times New Roman',
        'font_size':13,
        'bold': True,
        'align': 'center',
        'valign': 'vcenter'
    })
    text = workbook.add_format({
        'font_name':'Times New Roman',
        'font_size':12,
    })
    th = workbook.add_format({
        'font_name':'Times New Roman',
        'font_size':12,
        'top':6,
        'bottom':6,
        "text_wrap": True,
        'align': 'center',
        'valign': 'vcenter'
    })
    worksheet1.write('F2', 'РАСЧЕТ', title)
    worksheet1.write('F3', f'потребления электроэнергии за {month} {year} года', title)
    worksheet1.write('A4', f'Организация: {organization.short_name}', text)
    worksheet1.write('A5', f'Кому: {counterparty_name}', text)
    table_header = (
        'Место установки счётчика',
        'Номер счетчика',
        'Новые показания',
        'Предыдущие показания',
        'Разность',
        'Коэф. тр-рмации',
        'Количество кВт*ч',
        'Вычет, кВт*ч',
        'Потери в линии, %',
        'Постоянные потери, кВт*ч',
        'Результат кВт*ч',
        'Начислено без НДС',
        'Начислено с НДС',
    )
    row = 6
    col = 0
    for item in table_header:
        worksheet1.write(row, col, item, th)
        col +=1
    worksheet1.set_column(0, 0, width=20)
    worksheet1.set_column(1, 2, width=12)
    worksheet1.set_column(3, 3, width=13)
    worksheet1.set_column(4, 4, width=10)
    worksheet1.set_column(5, 5, width=9)
    worksheet1.set_column(6, 6, width=12)
    worksheet1.set_column(8, 8, width=11)
    worksheet1.set_column(9, 9, width=12)
    worksheet1.set_column(10, 10, width=10)
    worksheet1.set_column(11, 12, width=11)

    sum_accrued = 0
    sum_accrued_nds = 0
    for calculation in calculations:
        row += 2
        col = 0
        calculation_info = (
            calculation.point.name,
            calculation.meter.number,
            calculation.readings,
            calculation.previous_readings,
            calculation.difference_readings,
            calculation.transformation_coefficient,
            calculation.amount,
            calculation.deductible_amount,
            calculation.losses,
            calculation.constant_losses,
            calculation.result_amount,
            calculation.accrued,
            calculation.accrued_NDS,
        )
        sum_accrued_nds += calculation.accrued_NDS
        sum_accrued += calculation.accrued
        for item in calculation_info:
            worksheet1.write(row, col, item, text)
            col +=1
    string_accrued_nds = get_string_by_number(round(sum_accrued_nds, 2))
    nds = sum_accrued_nds - sum_accrued
    string_nds = get_string_by_number(round(nds, 2))

    row += 2
    worksheet1.write(row, 4, 'ВСЕГО:', text)
    if len(calculations) > 1:
        worksheet1.write_formula(row, 6, '=SUM(G9:{0}{1})'.format('G', row-1), text)
        worksheet1.write_formula(row, 7, '=SUM(H9:{0}{1})'.format('H', row-1), text)
        worksheet1.write_formula(row, 9, '=SUM(J9:{0}{1})'.format('J', row-1), text)
        worksheet1.write_formula(row, 10, '=SUM(K9:{0}{1})'.format('K', row-1), text)
    worksheet1.write_formula(row, 11, '=SUM(L9:{0}{1})'.format('L', row-1), text)
    worksheet1.write_formula(row, 12, '=SUM(M9:{0}{1})'.format('M', row-1), text)
    worksheet1.write(row+1, 4, 'в том числе НДС:', text)
    worksheet1.write_formula(row+1, 12, '={0}{1} - {2}{1}'.format('M', row+1, 'L'), text)
    worksheet1.write(row+4, 6, f'{user.post}', text)
    worksheet1.write(row+4, 10, f'{user_name}', text)

    if point.contract.agreement_type == 'Dogovor':
        agreement = 'договору'
    else:
        agreement = 'контракту'

    worksheet2 = workbook.add_worksheet('Акт')
    worksheet2.write('A1', f'Исполнитель: {organization.short_name} ИНН {organization.tax_identification_number} КПП {organization.registration_reason_code}', text)
    worksheet2.write('A2', f'Адрес: {organization.address} тел. {organization.phone_number}', text)
    worksheet2.write('F4', 'Акт приёма-передачи №', title)
    worksheet2.write('F5', f'по {agreement} №{point.contract.title} от {conclusion_date}', title)
    worksheet2.write('A7', f'Покупатель: {counterparty_name}', text)
    table_header2 = (
        'Наименование услуг, товара',
        'Единица измерения',
        'Количество',
        'Цена за единицу',
        'Стоимость без НДС',
        'НДС, %',
        'Сумма НДС',
        'Стоимость с НДС',
    )
    row2 = 8
    col2 = 0
    for item in table_header2:
        worksheet2.write(row2, col2, item, th)
        worksheet2.set_column(row2, col2, width=12)
        col2 +=1
    worksheet2.set_column(0, 0, width=25)
    worksheet2.write('A10', 'Эл/энергия (нерег.цены)', text)
    worksheet2.write('B10', 'кВт*ч', text)
    if len(calculations) > 1:
        worksheet2.write('C10', '=Расчет!{0}{1}'.format('G', row+1), text)
    else:
        worksheet2.write('C10', '=Расчет!{0}{1}'.format('G', row-1), text)
    worksheet2.write('D10', f'{calculation.tariff1}', text)
    worksheet2.write('E10', '=Расчет!{0}{1}'.format('L', row+1), text)
    worksheet2.write('F10', f'{NDS}', text)
    worksheet2.write('G10', '=Расчет!{0}{1}'.format('M', row+2), text)
    worksheet2.write('H10', '=Расчет!{0}{1}'.format('M', row+1), text)
    worksheet2.write('A12', f'Всего на сумму {string_accrued_nds}', text)
    worksheet2.write('A13', f'в т.ч. НДС {NDS}% - {string_nds}', text)
    worksheet2.write('A15', 'Покупатель претензий по объёму и качеству электроэнергии претензий не имеет.', text)
    worksheet2.write('B18', f'Исполнитель ________ {user_name}', text)
    worksheet2.write('F18', 'Покупатель ________ ', text)
    worksheet2.write('C19', 'м.п.', text)
    worksheet2.write('G19', 'м.п.', text)
    worksheet2.write('B21', f'Доверенность №{user.letter_of_attorney}', text)

    workbook.close()
    xlsx_data = output.getvalue()
    return xlsx_data


def get_previous_readings(point_id):
    calculation = Calculation.objects.filter(point=point_id).first()
    if calculation is not None:
        previous_readings = calculation.readings
    else:
        previous_readings = 0
    return previous_readings


def get_cumulative_statement_of_electricity_consumption(year):
    earlist_calculation = Calculation.objects.earliest('entry_date')
    years = [i for i in range(int(date.today().strftime('%Y')), int(earlist_calculation.entry_date.strftime('%Y')) - 1, -1)]
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    yearly_consumptions = []
    yearly_monye_consumptions = []
    amounts = [0] * 12
    monye_amounts = [0] * 12
    for counterparty in Counterparty.objects.all().prefetch_related("contracts__points__calculations"):
        for contract in counterparty.contracts.all().filter((Q(сompletion_date=None) | Q(сompletion_date__year=year)) & Q(conclusion_date__year__lte=year)):
            result_amounts = [0] * 12
            result_monye_amounts = [0] * 12
            for point in contract.points.all():
                for calculation in point.calculations.all().filter(entry_date__year=year):
                    result_amounts[int(calculation.entry_date.strftime('%m')) - 1] += int(calculation.result_amount)
                    result_monye_amounts[int(calculation.entry_date.strftime('%m')) - 1] += calculation.accrued_NDS
            amounts = [x+y for x, y in zip(amounts, result_amounts)]
            yearly_consumption = dict(zip(months, result_amounts))
            yearly_consumption['sum'] = sum(result_amounts)
            yearly_consumption['counterparty'] = counterparty
            yearly_consumption['contract'] = contract
            yearly_consumptions.append(yearly_consumption)
            monye_amounts = [round((x + y), 2) for x, y in zip(monye_amounts, result_monye_amounts)]
            yearly_monye_consumption = dict(zip(months, result_monye_amounts))
            yearly_monye_consumption['sum'] = sum(result_monye_amounts)
            yearly_monye_consumption['counterparty'] = counterparty
            yearly_monye_consumption['contract'] = contract
            yearly_monye_consumptions.append(yearly_monye_consumption)
    monthly_amounts = dict(zip(months, amounts))
    yearly_amount = sum(amounts)
    monthly_monye_amounts = dict(zip(months, monye_amounts))
    yearly_monye_amount = round(sum(monye_amounts), 2)
    cumulative_statement = {
        'years': years,
        'yearly_consumptions': yearly_consumptions,
        'monthly_amounts': monthly_amounts,
        'yearly_amount': yearly_amount,
        'yearly_monye_consumptions': yearly_monye_consumptions,
        'monthly_monye_amounts': monthly_monye_amounts,
        'yearly_monye_amount': yearly_monye_amount,
    }
    return cumulative_statement


def create_xlsx_document_yearly_consumptions(year):
    cumulative_statement = get_cumulative_statement_of_electricity_consumption(year)
    yearly_consumptions = cumulative_statement['yearly_consumptions']
    yearly_monye_consumptions = cumulative_statement['yearly_monye_consumptions']
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output)
    title = workbook.add_format({
        'font_name':'Times New Roman',
        'font_size':13,
        'bold': True,
        'align': 'center',
        'valign': 'vcenter'
    })
    text = workbook.add_format({
        'font_name':'Times New Roman',
        'font_size':13,
    })
    th = workbook.add_format({
        'font_name':'Times New Roman',
        'font_size':13,
        'top':6,
        'bottom':6,
        "text_wrap": True,
        'align': 'center',
        'valign': 'vcenter'
    })
    table_header = (
        'Наименование контрагента',
        'Номер договора',
        'Январь',
        'Февраль',
        'Март',
        'Апрель',
        'Май',
        'Июнь',
        'Июль',
        'Август',
        'Сентябрь',
        'Октябрь',
        'Ноябрь',
        'Декабрь',
        'Всего за период',
    )
    columns = ['C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O']

    worksheet1 = workbook.add_worksheet('кВт-ч')
    worksheet1.write('F2', 'Накопительная ведомость', title)
    worksheet1.write('F3', f'потребления электроэнергии за {year} год', title)
    worksheet1.write('F4', f'по всем организациям', title)
    row1 = 5
    col1 = 0
    for item in table_header:
        worksheet1.write(row1, col1, item, th)
        worksheet1.set_column(row1, col1, width=12)
        col1 +=1
    for yearly_consumption in yearly_consumptions:
        row1 += 1
        col1 = 0
        info = (
            yearly_consumption['counterparty'].short_name,
            yearly_consumption['contract'].title,
            yearly_consumption['January'],
            yearly_consumption['February'],
            yearly_consumption['March'],
            yearly_consumption['April'],
            yearly_consumption['May'],
            yearly_consumption['June'],
            yearly_consumption['July'],
            yearly_consumption['August'],
            yearly_consumption['September'],
            yearly_consumption['October'],
            yearly_consumption['November'],
            yearly_consumption['December'],
        )
        for item in info:
            worksheet1.write(row1, col1, item, text)
            col1 +=1
        worksheet1.write_formula(
            row1,
            col1,
            '=SUM({0}{1}:{2}{1})'.format('C', row1 + 1, 'N'),
            text
        )
    row1 += 1
    worksheet1.write(row1, 1, 'ВСЕГО:', text)
    for column in columns:
        worksheet1.write_formula(
            row1,
            columns.index(column) + 2,
            '=SUM({0}{1}:{0}{2})'.format(
                column,
                row1 - len(yearly_consumptions) + 1,
                row1
            ),
            text
        )
    
    worksheet2 = workbook.add_worksheet('Рубли')
    worksheet2.write('F2', 'Накопительная ведомость стоимости', title)
    worksheet2.write('F3', f'потребления электроэнергии за {year} год', title)
    worksheet2.write('F4', f'по всем организациям', title)
    row2 = 5
    col2 = 0
    for item in table_header:
        worksheet2.write(row2, col2, item, th)
        worksheet2.set_column(row2, col2, width=12)
        col2 +=1
    for yearly_monye_consumption in yearly_monye_consumptions:
        row2 += 1
        col2 = 0
        info = (
            yearly_monye_consumption['counterparty'].short_name,
            yearly_monye_consumption['contract'].title,
            yearly_monye_consumption['January'],
            yearly_monye_consumption['February'],
            yearly_monye_consumption['March'],
            yearly_monye_consumption['April'],
            yearly_monye_consumption['May'],
            yearly_monye_consumption['June'],
            yearly_monye_consumption['July'],
            yearly_monye_consumption['August'],
            yearly_monye_consumption['September'],
            yearly_monye_consumption['October'],
            yearly_monye_consumption['November'],
            yearly_monye_consumption['December'],
        )
        for item in info:
            worksheet2.write(row2, col2, item, text)
            col2 +=1
        worksheet2.write_formula(
            row2,
            col2,
            '=SUM({0}{1}:{2}{1})'.format('C', row2 + 1, 'N'),
            text
        )
    row2 += 1
    worksheet2.write(row2, 1, 'ВСЕГО:', text)
    for column in columns:
        worksheet2.write_formula(
            row2,
            columns.index(column) + 2,
            '=SUM({0}{1}:{0}{2})'.format(
                column,
                row2 - len(yearly_monye_consumptions) + 1,
                row2
            ),
            text
        )

    workbook.close()
    xlsx_data = output.getvalue()
    return xlsx_data
