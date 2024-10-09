from django import forms

from .models import Document ,Contract, Counterparty


class DateInput(forms.DateInput):
    input_type = 'date'
    format = '%Y-%m-%d'


class DocumentForm(forms.ModelForm):
    conclusion_date = forms.DateField(
        label='Дата заключения договора',
        required=True,
        widget=DateInput({'class': 'form-control'}),
        localize=True,
    )
    class Meta:
        model = Document
        fields = (
            'title',
            'conclusion_date',
            'file',
        )


class ContractForm(forms.ModelForm):
    conclusion_date = forms.DateField(
        label='Дата заключения договора',
        required=True,
        widget=DateInput({'class': 'form-control'}),
        localize=True,
    )
    сompletion_date = forms.DateField(
        label='Дата завершения работ',
        required=False,
        widget=DateInput({'class': 'form-control'}),
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
            'tax_identification_number',
            'registration_reason_code',
            'job_title',
            'person_full_name',
        )
