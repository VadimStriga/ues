from django.contrib import admin

from .models import Document ,Contract, Counterparty


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = (
        'contract',
        'title',
        'file',
        'conclusion_date',
    )


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = (
        'counterparty',
        'title',
        'conclusion_date',
        'contract_price',
        'purchase_code',
        'description',
        'сompletion_date',
        'actual_cost',
    )


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
