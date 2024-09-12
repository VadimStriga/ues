from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from counterparties.models import Contract
from .forms import (CalculationForm,
                    CurrentTransformerForm,
                    ElectricityMeterForm,
                    ElectricityMeteringPointForm,
                    TariffForm)
from .models import (NDS,
                     Calculation,
                     CurrentTransformer,
                     ElectricityMeter,
                     ElectricityMeteringPoint,
                     Tariff)
from .utils import (calculation_accrued,
                    calculation_result_amount,
                    calculation_tariff)


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
    readings_form = CalculationForm()
    if len(calculations) != 0:
        previous_readings = calculations[0].readings
    else:
        previous_readings = 0
    meters = ElectricityMeter.objects.filter(point=point_id).filter(is_active=True)
    current_meter_number = meters[0].number
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
        'readings_form': readings_form,
        'meters': meters,
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
def add_readings(request, point_id):
    point = get_object_or_404(ElectricityMeteringPoint, pk=point_id)
    readings_form = CalculationForm(request.POST or None)
    if readings_form.is_valid():
        calculation = readings_form.save(commit=False)
        calculation.point = point
        calculation.meter = ElectricityMeter.objects.filter(point=point_id).filter(is_active=True)[0]
        calculation.previous_entry_date = Calculation.objects.filter(point=point_id)[0].entry_date
        calculation.previous_readings = Calculation.objects.filter(point=point_id)[0].readings
        calculation.difference_readings = calculation.readings - calculation.previous_readings
        calculation.transformation_coefficient = point.transformation_coefficient
        calculation.amount = calculation.difference_readings * calculation.transformation_coefficient
        calculation.deductible_amount = 0
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
    context = {
        'readings_form': readings_form,
    }
    return render(request, 'accounting/add_readings.html', context)


@login_required
def del_readings(request, point_id, calculation_id):
    calculation = get_object_or_404(Calculation, pk=calculation_id)
    calculation.delete()
    return redirect('accounting:point_detail', point_id = point_id)
