from django.contrib import admin

from .models import Counterparty


@admin.register(Counterparty)
class CounterpartyAdmin(admin.ModelAdmin):
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
    list_display_links = ('full_name', 'short_name',)
    list_filter = ('full_name',)
    search_fields = ('full_name', 'short_name', 'main_state_registration_number')
