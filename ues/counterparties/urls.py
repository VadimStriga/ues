from django.urls import path

from . import views


app_name = 'counterparties'

urlpatterns = [
    path(
        'contract_detail/<int:contract_id>/document_create/',
        views.add_document,
        name='add_document',
    ),
    path(
        'contract_detail/<int:contract_id>/document/<int:document_id>/delete/',
        views.delete_document,
        name='delete_document',
    ),
    path(
        '<int:counterparty_id>/contract_create/',
        views.contract_create,
        name='contract_create'
    ),
    path(
        '<int:counterparty_id>/contract_detail/<int:contract_id>/delete/',
        views.contract_delete,
        name='contract_delete'
    ),
    path(
        'contract_detail/<int:contract_id>/',
        views.contract_detail,
        name='contract_detail'
    ),
    path(
        'contract_detail/<int:contract_id>/edit/',
        views.contract_edit,
        name='contract_edit'
    ),
    path(
        'contracts_list/',
        views.contracts_list,
        name='contracts_list',
    ),
    path(
        'create/',
        views.counterparty_create,
        name='counterparty_create',
    ),
    path(
        '<int:counterparty_id>/delete/',
        views.counterparty_delete,
        name='counterparty_delete',
    ),
    path(
        '<int:counterparty_id>/',
        views.counterparty_detail,
        name='counterparty_detail',
    ),
    path(
        '<int:counterparty_id>/edit/',
        views.counterparty_edit,
        name='counterparty_edit',
    ),
    path(
        'counterparties_list/',
        views.counterparties_list,
        name='counterparties_list'
    ),
    path(
        'contract_detail/<int:contract_id>/comments/create/',
        views.comment_create,
        name='comment_contract_create',
    ),
    path(
        'contract_detail/<int:contract_id>/comments/<int:comment_id>/delete/',
        views.comment_delete,
        name='comment_contract_delete',
    ),
    path(
        'contract_detail/<int:contract_id>/comments/<int:comment_id>/edit/',
        views.comment_edit,
        name='comment_contract_edit',
    ),
    path(
        '<int:counterparty_id>/comments/create/',
        views.comment_create,
        name='comment_counterparty_create',
    ),
    path(
        '<int:counterparty_id>/comments/<int:comment_id>/delete/',
        views.comment_delete,
        name='comment_counterparty_delete',
    ),
    path(
        '<int:counterparty_id>/comments/<int:comment_id>/edit/',
        views.comment_edit,
        name='comment_counterparty_edit',
    ),
]
