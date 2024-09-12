from django.contrib import admin

from .models import (Calculation,
                     CurrentTransformer,
                     ElectricityMeter,
                     ElectricityMeteringPoint,
                     Tariff)


@admin.register(Calculation)
class CalculationAdmin(admin.ModelAdmin):
    list_display = (
        'point',
        'meter',
        'entry_date',
        'readings',
        'previous_entry_date',
        'previous_readings',
        'difference_readings',
        'transformation_coefficient',
        'amount',
        'deductible_amount',
        'losses',
        'constant_losses',
        'result_amount',
        'tariff1',
        'tariff2',
        'tariff3',
        'margin',
        'accrued',
        'accrued_NDS',
    )


@admin.register(CurrentTransformer)
class CurrentTransformerAdmin(admin.ModelAdmin):
    list_display = (
        'is_active',
        'mark',
        'number',
        'installation_date',
        'date_of_next_verification',
        'point',
    )


@admin.register(ElectricityMeter)
class ElectricityMeterAdmin(admin.ModelAdmin):
    list_display = (
        'is_active',
        'mark',
        'number',
        'installation_date',
        'date_of_next_verification',
        'point',
    )


@admin.register(ElectricityMeteringPoint)
class ElectricityMeteringPointAdmin(admin.ModelAdmin):
    list_display = (
        'contract',
        'name',
        'location',
        'power_supply',
        'type_of_accounting',
        'tariff',
        'margin',
        'losses',
        'constant_losses',
        'transformation_coefficient',
    )


@admin.register(Tariff)
class TarifAdmin(admin.ModelAdmin):
    list_display = (
        'pub_date',
        'begin_tariff_period',
        'end_tariff_period',
        'high_voltage_tariff',
        'medium_voltage_tariff_1',
        'medium_voltage_tariff_2',
        'low_voltage_tariff',
        'urban_tariff_1',
        'urban_tariff_2',
        'urban_tariff_3',
        'rural_tariff_1',
        'rural_tariff_2',
        'rural_tariff_3',
    )
