from django.contrib import admin

from .models import Organization


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
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
