from django.urls import path

from . import views

app_name = 'counterparties'

urlpatterns = [
    path('', views.index, name='index'),
    path(
        'counterparties/<int:counterparty_id>/contract_create/',
        views.contract_create,
        name='contract_create'
    ),
    path(
        'counterparties/contract_detail/<int:contract_id>/',
        views.contract_detail,
        name='contract_detail'
    ),
    path(
        'counterparties/contract_detail/<int:contract_id>/edit/',
        views.contract_edit,
        name='contract_edit'
    ),
    path(
        'counterparties/contract_detail/<int:contract_id>/delete/',
        views.contract_delete,
        name='contract_delete'
    ),
    path(
        'contracts_list/',
        views.contracts_list,
        name='contracts_list',
    ),
    path(
        'counterparties/create/',
        views.counterparty_create,
        name='counterparty_create',
    ),
    path(
        'counterparties/<int:counterparty_id>/',
        views.counterparty_detail,
        name='counterparty_detail',
    ),
    path(
        'counterparties/<int:counterparty_id>/edit',
        views.counterparty_edit,
        name='counterparty_edit',
    ),
    path(
        'counterparties/<int:counterparty_id>/delete',
        views.counterparty_delete,
        name='counterparty_delete',
    ),
]
