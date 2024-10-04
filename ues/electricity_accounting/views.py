from datetime import date
from django.http import HttpResponse

from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from transliterate import translit
import xlsxwriter

from counterparties.models import Contract
from .forms import (CalculationForm,
                    CurrentTransformerForm,
                    ElectricityMeterForm,
                    ElectricityMeteringPointForm,
                    TariffForm,
                    InterconnectedPoints)
from .models import (NDS,
                     Calculation,
                     CurrentTransformer,
                     InterconnectedPoints,
                     ElectricityMeter,
                     ElectricityMeteringPoint,
                     Tariff)
from .utils import (get_deductible_amount,
                    calculation_accrued,
                    calculation_previous_entry_date,
                    calculation_previous_readings,
                    calculation_result_amount,
                    calculation_tariff,
                    create_xlsx_document)


NUMBER_OF_POINTS = 25


@login_required
def meter_create(request, point_id):
    point = get_object_or_404(ElectricityMeteringPoint, pk=point_id)
    form = ElectricityMeterForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        meter=form.save(commit=False)
        meter.point = point
        meter.save()
        return redirect('accounting:point_detail', point_id = point_id)
    context = {
        'form':form,
    }
    return render(request, 'accounting/meter_create.html', context)


@login_required
def meter_delete(request, point_id, meter_id):
    meter = get_object_or_404(ElectricityMeter, pk=meter_id)
    meter.delete()
    return redirect('accounting:point_detail', point_id = point_id)


@login_required
def meter_edit(request, point_id, meter_id):
    meter = get_object_or_404(ElectricityMeter, pk=meter_id)
    form = ElectricityMeterForm(
        request.POST or None,
        files=request.FILES or None,
        instance=meter
    )
    if form.is_valid():
        form.save()
        return redirect('accounting:point_detail', point_id = point_id)
    context = {
        'form':form,
        'meter': meter,
        'is_edit': True,
    }
    return render(request, 'accounting/meter_create.html', context)


@login_required
def transformer_create(request, point_id):
    point = get_object_or_404(ElectricityMeteringPoint, pk=point_id)
    form = CurrentTransformerForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        transformer=form.save(commit=False)
        transformer.point = point
        transformer.save()
        return redirect('accounting:point_detail', point_id = point_id)
    context = {
        'form':form,
    }
    return render(request, 'accounting/transformer_create.html', context)


@login_required
def transformer_delete(request, point_id, transformer_id):
    transformer = get_object_or_404(CurrentTransformer, pk=transformer_id)
    transformer.delete()
    return redirect('accounting:point_detail', point_id = point_id)


@login_required
def transformer_edit(request, point_id, transformer_id):
    transformer = get_object_or_404(CurrentTransformer, pk=transformer_id)
    form = CurrentTransformerForm(
        request.POST or None,
        files=request.FILES or None,
        instance=transformer
    )
    if form.is_valid():
        form.save()
        return redirect('accounting:point_detail', point_id = point_id)
    context = {
        'form':form,
        'transformer': transformer,
        'is_edit': True,
    }
    return render(request, 'accounting/transformer_create.html', context)


@login_required
def point_create(request, contract_id):
    contract = get_object_or_404(Contract, pk=contract_id)
    form = ElectricityMeteringPointForm(request.POST or None)
    if form.is_valid():
        point = form.save(commit=False)
        point.contract = contract
        point.save()
        return redirect('counterparties:contract_detail', contract_id=contract_id,)
    context = {
            'form': form,
        }
    return render(request, 'accounting/point_create.html', context)


def point_detail(request, point_id):
    point = get_object_or_404(ElectricityMeteringPoint, pk=point_id)
    calculations = Calculation.objects.filter(point=point_id)
    calculation_form = CalculationForm()
    td = date.today()
    deductible_amount = get_deductible_amount(point_id, td)
    if len(calculations) != 0:
        previous_readings = calculations[0].readings
    else:
        previous_readings = 0
    meters = ElectricityMeter.objects.filter(point=point_id).filter(is_active=True)
    if len(meters) != 0:
        current_meter_number = meters[0].number
        alert_flag = False
    else:
        current_meter_number = 0
        alert_flag = True
    old_meters = ElectricityMeter.objects.filter(point=point_id).filter(is_active=False)
    transformers = CurrentTransformer.objects.filter(point=point_id).filter(is_active=True)
    old_transformers = CurrentTransformer.objects.filter(point=point_id).filter(is_active=False)
    tariff1, tariff2, tariff3, is_population = calculation_tariff(point_id)
    context = {
        'point': point,
        'calculations': calculations,
        'previous_readings': previous_readings,
        'is_population': is_population,
        'tariff1': tariff1,
        'tariff2': tariff2,
        'tariff3': tariff3,
        'calculation_form': calculation_form,
        'deductible_amount': deductible_amount,
        'meters': meters,
        'alert_flag': alert_flag,
        'current_meter_number': current_meter_number,
        'old_meters': old_meters,
        'transformers': transformers,
        'old_transformers': old_transformers,
    }
    return render(request, 'accounting/point_detail.html', context)


@login_required
def point_delete(request, point_id):
    point = get_object_or_404(ElectricityMeteringPoint, pk=point_id)
    point.delete()
    return redirect('counterparties:contract_detail', contract_id=point.contract.id)


@login_required
def point_edit(request, point_id):
    point = get_object_or_404(ElectricityMeteringPoint, pk=point_id)
    form = ElectricityMeteringPointForm(request.POST or None, instance=point)
    if form.is_valid():
        form.save()
        return redirect('accounting:point_detail', point_id=point.id)
    context = {
        'form': form,
        'point': point,
        'is_edit': True,
    }
    return render(request, 'accounting/point_create.html', context)


def points_list(request):
    points = ElectricityMeteringPoint.objects.all()
    paginator = Paginator(points, NUMBER_OF_POINTS)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        "page_obj": page_obj,
    }
    return render(request, "accounting/points_list.html", context)


def tariffs_list(request):
    tariffs = Tariff.objects.all()
    paginator = Paginator(tariffs, NUMBER_OF_POINTS)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        "page_obj": page_obj,
    }
    return render(request, "accounting/tariffs_list.html", context)


@login_required
def add_calculation(request, point_id):
    point = get_object_or_404(ElectricityMeteringPoint, pk=point_id)
    calculation_form = CalculationForm(request.POST or None)
    try:
        if calculation_form.is_valid():
            calculation = calculation_form.save(commit=False)
            calculation.point = point
            calculation.meter = ElectricityMeter.objects.filter(point=point_id).filter(is_active=True)[0]
            calculation.previous_entry_date = calculation_previous_entry_date(point_id)
            calculation.previous_readings = calculation_previous_readings(point_id, calculation.readings)
            calculation.difference_readings = round((calculation.readings - calculation.previous_readings), 2)
            calculation.transformation_coefficient = point.transformation_coefficient
            calculation.amount = calculation.difference_readings * calculation.transformation_coefficient
            calculation.deductible_amount = get_deductible_amount(point_id, calculation.entry_date)
            calculation.losses = point.losses
            calculation.constant_losses = point.constant_losses
            calculation.result_amount = calculation_result_amount(calculation.amount,
                                                                  calculation.deductible_amount,
                                                                  calculation.losses,
                                                                  calculation.constant_losses)
            calculation.tariff1, calculation.tariff2, calculation.tariff3, is_population = calculation_tariff(point_id)
            calculation.margin = point.margin
            calculation.accrued = calculation_accrued(calculation.result_amount,
                                                      calculation.tariff1,
                                                      calculation.tariff2,
                                                      calculation.tariff3,
                                                      calculation.margin)
            calculation.accrued_NDS = round((calculation.accrued + calculation.accrued * NDS / 100), 2)
            calculation.save()
            return redirect('accounting:point_detail', point_id = point_id)
    except IndexError:
        return redirect('accounting:point_detail', point_id = point_id)


@login_required
def del_calculation(request, point_id, calculation_id):
    calculation = get_object_or_404(Calculation, pk=calculation_id)
    calculation.delete()
    return redirect('accounting:point_detail', point_id = point_id)


@login_required
def add_lower_point(request, point_id):
    point = get_object_or_404(ElectricityMeteringPoint, pk=point_id)
    form = InterconnectedPoints(request.POST or None)
    if form.is_valid():
        deduction_amount = form.save(commit=False)
        deduction_amount.head_point = point
        deduction_amount.save()
        return redirect('accounting:point_detail', point_id = point_id)


def download_xlsx_document(request, point_id, calculation_id):
    calculation = get_object_or_404(Calculation, pk=calculation_id)
    point = get_object_or_404(ElectricityMeteringPoint, pk=point_id)
    counterparty = point.contract.counterparty.short_name
    counterparty_translit = translit(counterparty, reversed=True)
    month = calculation.entry_date.strftime('%B')
    year = calculation.entry_date.strftime('%Y')
    filename = f'Raschet za {month} {year} {counterparty_translit}.xlsx'
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = f'attachment; filename={filename}'
    xlsx_data = create_xlsx_document(request, point_id, calculation_id)
    response.write(xlsx_data)
    return response
