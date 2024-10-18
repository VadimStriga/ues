from django.shortcuts import redirect

from .models import Contract, Counterparty
from electricity_accounting.models import ElectricityMeteringPoint


def get_redirect_url(id):    
    if 'counterparty_id' in id.keys():
        counterparty_id = id['counterparty_id']
        redirect_url = redirect('counterparties:counterparty_detail', counterparty_id=counterparty_id)
    if 'contract_id' in id.keys():
        contract_id = id['contract_id']
        redirect_url = redirect('counterparties:contract_detail', contract_id=contract_id)
    if 'point_id' in id.keys():
        point_id = id['point_id']
        redirect_url = redirect('accounting:point_detail', point_id=point_id)
    return redirect_url


def get_object_class_and_redirect_url(value, object_id):
    if value == 'counterparty_id':
        object_class = Counterparty
        redirect_url = redirect('counterparties:counterparty_detail', counterparty_id=object_id)
    if value == 'contract_id':
        object_class = Contract
        redirect_url = redirect('counterparties:contract_detail', contract_id=object_id)
    if value == 'point_id':
        object_class = ElectricityMeteringPoint
        redirect_url = redirect('accounting:point_detail', point_id=object_id)
    return object_class, redirect_url
