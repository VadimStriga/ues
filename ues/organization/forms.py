from django import forms

from .models import Organization


class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
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
