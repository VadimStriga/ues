from django import forms

from .models import (Calculation,
                     CurrentTransformer,
                     ElectricityMeter,
                     ElectricityMeteringPoint,
                     Tariff)


class DateInput(forms.DateInput):
    input_type = "date"
    format = "%Y-%m-%d"


class BooleanDropdown(forms.widgets.Select):
    def __init__(self, attrs=None):
        choices = (
            ('True', 'Действующий'),
            ('False', 'Недействующий'),
        )
        super().__init__(attrs=attrs, choices=choices)

    def value_from_datadict(self, data, files, name):
        value = super().value_from_datadict(data, files, name)
        return {'True': True, 'False': False}.get(value)


class CalculationForm(forms.ModelForm):
    entry_date = forms.DateField(
        label='Дата снятия показаний',
        required=True,
        widget=DateInput({'class': 'form-control'}),
        localize=True,
    )
    class Meta:
        model = Calculation
        fields = (
            'entry_date',
            'readings',
        )


class CurrentTransformerForm(forms.ModelForm):
    installation_date = forms.DateField(
        label='Дата установки',
        required=True,
        widget=DateInput({'class': 'form-control'}),
        localize=True,
    )
    date_of_next_verification =  forms.DateField(
        label='Дата следующей поверки',
        required=True,
        widget=DateInput({'class': 'form-control'}),
        localize=True,
    )
    class Meta:
        model = CurrentTransformer
        fields = (
            'is_active',
            'mark',
            'number',
            'installation_date',
            'date_of_next_verification',
            'photo',
        )
        widgets = {
            'is_active': BooleanDropdown(),
        }


class ElectricityMeterForm(forms.ModelForm):
    installation_date = forms.DateField(
        label='Дата установки',
        required=True,
        widget=DateInput({'class': 'form-control'}),
        localize=True,
    )
    date_of_next_verification =  forms.DateField(
        label='Дата следующей поверки',
        required=True,
        widget=DateInput({'class': 'form-control'}),
        localize=True,
    )
    class Meta:
        model = ElectricityMeter
        fields = (
            'is_active',
            'mark',
            'number',
            'installation_date',
            'date_of_next_verification',
            'photo',
        )
        widgets = {
            'is_active': BooleanDropdown(),
        }


class ElectricityMeteringPointForm(forms.ModelForm):

    class Meta:
        model = ElectricityMeteringPoint
        fields = (
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


class TariffForm(forms.ModelForm):
    begin_tariff_period = forms.DateField(
        label='Начало периода действия тарифов',
        required=True,
        widget=DateInput({'class': 'form-control'}),
        localize=True,
    )
    end_tariff_period = forms.DateField(
        label='Начало периода действия тарифов',
        required=True,
        widget=DateInput({'class': 'form-control'}),
        localize=True,
    )
    class Meta:
        model = Tariff
        fields = (
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
