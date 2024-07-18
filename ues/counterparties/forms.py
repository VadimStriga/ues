from django import forms

from .models import Contract, Counterparty


class ContractDateInput(forms.DateInput):
    input_type = 'date'
    format = '%Y-%m-%d'


class ContractForm(forms.ModelForm):
    conclusion_date = forms.DateField(
        label='Дата заключения договора',
        required=True,
        widget = forms.SelectDateWidget,
        localize=True,
    )
    сompletion_date = forms.DateField(
        label='Дата завершения работ',
        required=False,
        widget = forms.SelectDateWidget,
        localize=True,
    )

    class Meta:
        model = Contract
        fields = (
            'title',
            'conclusion_date',
            'contract_price',
            'purchase_code',
            'description',
            'сompletion_date',
            'actual_cost',
        )


class CounterpartyForm(forms.ModelForm):
    class Meta:
        model = Counterparty
        fields = (
            'full_name',
            'short_name',
            'address',
            'phone_number',
            'email',
            'main_state_registration_number',
            'registration_reason_code',
            'tax_identification_number',
            'job_title',
            'person_full_name',
        )
