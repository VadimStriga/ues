from django.urls import path

from . import views


app_name = 'organization'

urlpatterns = [
    path(
        'organization_create/',
        views.organization_create,
        name='organization_create',
    ),
    path(
        'organization_detail/<int:organization_id>/delete/',
        views.organization_delete,
        name='organization_delete',
    ),
    path(
        'organization_detail/<int:organization_id>/edit/',
        views.organization_edit,
        name='organization_edit',
    ),
    path(
        'organization/',
        views.organization_detail,
        name='organization_detail',
    ),
    path(
        '',
        views.IndexView.as_view(),
        name='about_organization',
    ),
]
