from django.urls import path

from . import views


app_name = 'accounting'

urlpatterns = [
    path(
        'point_detail/<int:point_id>/meter_create/',
        views.meter_create,
        name='meter_create',        
    ),
    path(
        'point_detail/<int:point_id>/meter/<int:meter_id>/delete/',
        views.meter_delete,
        name='meter_delete',        
    ),
    path(
        'point_detail/<int:point_id>/meter/<int:meter_id>/edit/',
        views.meter_edit,
        name='meter_edit',        
    ),
     path(
        'point_detail/<int:point_id>/transformer_create/',
        views.transformer_create,
        name='transformer_create',        
    ),
    path(
        'point_detail/<int:point_id>/transformer/<int:transformer_id>/delete/',
        views.transformer_delete,
        name='transformer_delete',        
    ),
    path(
        'point_detail/<int:point_id>/transformer/<int:transformer_id>/edit/',
        views.transformer_edit,
        name='transformer_edit',        
    ),
    path(
        'counterparties/contract_detail/<int:contract_id>/point_create/',
        views.point_create,
        name='point_create',
    ),
    path(
        'point_detail/<int:point_id>/',
        views.point_detail,
        name='point_detail',
    ),
    path(
        'point_detail/<int:point_id>/delete/',
        views.point_delete,
        name='point_delete',
    ),
    path(
        'point_detail/<int:point_id>/edit/',
        views.point_edit,
        name='point_edit',
    ),
    path(
        'points_list/',
        views.points_list,
        name='points_list',
    ),
    path(
        'tariffs_list/',
        views.tariffs_list,
        name='tariffs_list',
    ),
    path(
        'point_detail/<int:point_id>/calculations/add_calculation/',
        views.add_calculation,
        name='add_calculation',
    ),
    path(
        'point_detail/<int:point_id>/calculations/<int:calculation_id>/delete/',
        views.del_calculation,
        name='del_calculation',
    ),
    path(
        'point_detail/<int:point_id>/',
        views.add_lower_point,
        name='add_lower_point',
    ),
]
