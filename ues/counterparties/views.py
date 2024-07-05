from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ContractForm, CounterpartyForm


from .models import Contract, Counterparty


def index(request):
    counterparties = Counterparty.objects.all()
    context = {
        'counterparties': counterparties,
    }
    return render(request, 'counterparties/index.html', context)


def contract_create(request, counterparty_id):
    form = ContractForm(request.POST or None)
    print(request)
    print(counterparty_id)
    if form.is_valid():
        contract = form.save(commit=False)
        contract.counterparty = get_object_or_404(Counterparty, pk=counterparty_id)
        contract.save()
        return redirect('counterparties:contract_detail', contract_id=contract.id,)
    context = {
        'form': form,
    }
    return render(request, 'counterparties/contract_create.html', context)


def contract_delete(request, contract_id):
    contract = get_object_or_404(Contract, pk=contract_id)
    contract.delete()
    return redirect('counterparties:index')


def contract_detail(request, contract_id):
    contract = get_object_or_404(Contract, pk=contract_id)
    context = {
        'contract': contract,
    }
    return render(request, 'counterparties/contract_detail.html', context)


def contract_edit(request, contract_id):
    contract = get_object_or_404(Contract, pk=contract_id)
    form = ContractForm(request.POST or None, instance=contract)
    if form.is_valid():
        form.save()
        return redirect(
            'counterparties:contract_detail',
            contract_id=contract.id
        )
    context = {
        'form': form,
        'contract': contract,
        'is_edit': True,
    }    
    return render(request, 'counterparties/contract_create.html', context)


def contracts_list(request):
    contracts = Contract.objects.all()
    print(contracts[0])
    context = {
        'contracts': contracts,
    }
    return render(request, 'counterparties/contracts_list.html', context)


@login_required
def counterparty_create(request):
    form = CounterpartyForm(request.POST or None)
    if form.is_valid():
        counterparty = form.save(commit=False)
        counterparty.save()
        return redirect('counterparties:counterparty_detail', counterparty_id=counterparty.id)
    context = {
        'form': form,
    }
    return render(request, 'counterparties/counterparty_create.html', context)


def counterparty_delete(request, counterparty_id):
    counterparty = get_object_or_404(Counterparty, pk=counterparty_id)
    counterparty.delete()
    return redirect('counterparties:index')


def counterparty_detail(request, counterparty_id):
    counterparty = get_object_or_404(Counterparty, pk=counterparty_id)
    contracts = Contract.objects.filter(counterparty=counterparty_id)
    context = {
        'counterparty': counterparty,
        'contracts': contracts,
    }
    return render(request, 'counterparties/counterperty_detail.html', context)


def counterparty_edit(request, counterparty_id):
    counterparty = get_object_or_404(Counterparty, pk=counterparty_id)
    form = CounterpartyForm(request.POST or None, instance=counterparty)
    if form.is_valid():
        counterparty.save()
        return redirect('counterparties:counterparty_detail', counterparty_id=counterparty.id)
    context = {
        'form': form,
        'counterparty': counterparty,
        'is_edit': True,
    }
    return render(request, 'counterparties/counterparty_create.html', context)
