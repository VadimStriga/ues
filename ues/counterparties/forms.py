from django import forms

from .models import Counterparty


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
