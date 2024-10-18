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
        'counterparties/contract_detail/<int:contract_id>/document/',
        views.add_document,
        name='add_document',
    ),
    path(
        'counterparties/contract_detail/<int:contract_id>/document/<int:document_id>/',
        views.delete_document,
        name='delete_document',
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
        'counterparties/<int:counterparty_id>/edit/',
        views.counterparty_edit,
        name='counterparty_edit',
    ),
    path(
        'counterparties/<int:counterparty_id>/delete/',
        views.counterparty_delete,
        name='counterparty_delete',
    ),
    path(
        'counterparties/counterparty_detail/<int:counterparty_id>/comments/create/',
        views.comment_create,
        name='comment_counterparty_create',
    ),
    path(
        'counterparties/counterparty_detail/<int:counterparty_id>/comments/<int:comment_id>/delete/',
        views.comment_delete,
        name='comment_counterparty_delete',
    ),
    path(
        'counterparties/counterparty_detail/<int:counterparty_id>/comments/<int:comment_id>/edit/',
        views.comment_edit,
        name='comment_counterparty_edit',
    ),
    path(
        'counterparties/contract_detail/<int:contract_id>/comments/create/',
        views.comment_create,
        name='comment_contract_create',
    ),
    path(
        'counterparties/contract_detail/<int:contract_id>/comments/<int:comment_id>/delete/',
        views.comment_delete,
        name='comment_contract_delete',
    ),
    path(
        'counterparties/contract_detail/<int:contract_id>/comments/<int:comment_id>/edit/',
        views.comment_edit,
        name='comment_contract_edit',
    ),
]
