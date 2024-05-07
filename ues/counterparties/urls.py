from django.urls import path

from . import views

app_name = 'counterparties'

urlpatterns = [
    path('', views.index, name='index'),
    path('counterparties/create/',
         views.counterparty_create,
         name='counterparty_create',),
    path('counterparties/<int:counterparty_id>/',
        views.counterparty_detail,
        name='counterparty_detail',),
]
