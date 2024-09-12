from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import DocumentForm ,ContractForm, CounterpartyForm
from .models import Document ,Contract, Counterparty
from electricity_accounting.models import ElectricityMeteringPoint


NUMBER_OF_COUNTERPARTIES = 25
NUMBER_OF_CONTRACTS = 25


def index(request):
    counterparties = Counterparty.objects.all()
    paginator = Paginator(counterparties, NUMBER_OF_COUNTERPARTIES)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'counterparties/index.html', context)


@login_required
def contract_create(request, counterparty_id):
    form = ContractForm(request.POST or None)
    if form.is_valid():
        contract = form.save(commit=False)
        contract.counterparty = get_object_or_404(Counterparty, pk=counterparty_id)
        contract.save()
        return redirect('counterparties:contract_detail', contract_id=contract.id,)
    context = {
        'form': form,
    }
    return render(request, 'counterparties/contract_create.html', context)


@login_required
def add_document(request, contract_id):
    contract = get_object_or_404(Contract, pk=contract_id)
    form = DocumentForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        document = form.save(commit=False)
        document.contract = contract
        document.save()
    return redirect('counterparties:contract_detail', contract_id=contract_id)


@login_required
def delete_document(request, contract_id, document_id):
    document = get_object_or_404(Document, pk=document_id)
    document.delete()
    return redirect('counterparties:contract_detail', contract_id=contract_id)


@login_required
def contract_delete(request, contract_id):
    contract = get_object_or_404(Contract, pk=contract_id)
    contract.delete()
    return redirect('counterparties:index')


def contract_detail(request, contract_id):
    contract = get_object_or_404(Contract, pk=contract_id)
    form = DocumentForm
    documents = Document.objects.filter(contract=contract_id)
    documents_count = Document.objects.filter(contract=contract_id).count()
    points = ElectricityMeteringPoint.objects.filter(contract=contract_id)
    context = {
        'contract': contract,
        'documents': documents,
        'documents_count': documents_count,
        'points': points,
        'form': form,
    }
    return render(request, 'counterparties/contract_detail.html', context)


@login_required
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
    paginator = Paginator(contracts, NUMBER_OF_CONTRACTS)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
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


@login_required
def counterparty_delete(request, counterparty_id):
    counterparty = get_object_or_404(Counterparty, pk=counterparty_id)
    counterparty.delete()
    return redirect('counterparties:index')


def counterparty_detail(request, counterparty_id):
    counterparty = get_object_or_404(Counterparty, pk=counterparty_id)
    contracts = Contract.objects.filter(counterparty=counterparty_id)
    contracts_count = Contract.objects.filter(counterparty=counterparty).count()
    points = ElectricityMeteringPoint.objects.filter(contract__in=contracts)
    context = {
        'counterparty': counterparty,
        'contracts': contracts,
        'contracts_count': contracts_count,
        'points': points,
    }
    return render(request, 'counterparties/counterperty_detail.html', context)


@login_required
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
