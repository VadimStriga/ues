from django.core.paginator import Paginator
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CommentForm, DocumentForm, ContractForm, CounterpartyForm
from .models import Comment, Document, Contract, Counterparty
from .utils import get_redirect_url, get_object_class_and_redirect_url
from electricity_accounting.models import ElectricityMeteringPoint


NUMBER_OF_OUTPUT_COUNTERPARTIES = 20
NUMBER_OF_OUTPUT_CONTRACTS = 20


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
def contract_delete(request, counterparty_id, contract_id):
    counterparty = get_object_or_404(Counterparty, pk=counterparty_id)
    contract = get_object_or_404(Contract, pk=contract_id)
    contract.delete()
    return redirect('counterparties:counterparty_detail', counterparty_id=counterparty.id)


def contract_detail(request, contract_id):
    contract = get_object_or_404(Contract, pk=contract_id)
    comment_form = CommentForm()
    comments = Comment.objects.filter(contract__pk=contract_id)
    form = DocumentForm()
    documents = Document.objects.filter(contract=contract_id)
    documents_count = Document.objects.filter(contract=contract_id).count()
    points = ElectricityMeteringPoint.objects.filter(contract=contract_id)
    context = {
        'comment_form': comment_form,
        'comments': comments,
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
    paginator = Paginator(contracts, NUMBER_OF_OUTPUT_CONTRACTS)
    page_number = request.GET.get('page')
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
    return redirect('counterparties:counterparties_list')


def counterparty_detail(request, counterparty_id):
    counterparty = get_object_or_404(Counterparty, pk=counterparty_id)
    comment_form = CommentForm()
    comments = Comment.objects.filter(counterparty__pk=counterparty_id)
    contracts = Contract.objects.filter(counterparty=counterparty_id)
    contracts_count = Contract.objects.filter(counterparty=counterparty).count()
    points = ElectricityMeteringPoint.objects.filter(contract__in=contracts)
    context = {
        'counterparty': counterparty,
        'comments': comments,
        'contracts': contracts,
        'contracts_count': contracts_count,
        'points': points,
        'comment_form': comment_form,
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


def counterparties_list(request):
    counterparties = Counterparty.objects.all()
    paginator = Paginator(counterparties, NUMBER_OF_OUTPUT_COUNTERPARTIES)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'counterparties/counterparties_list.html', context)


@login_required
def comment_create(request, **id):
    value = next(iter(id))
    object_id = id.get(value)
    object_class, redirect_url = get_object_class_and_redirect_url(value, object_id)
    content_type = ContentType.objects.get_for_model(object_class)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.content_type = content_type
        comment.object_id = object_id
        comment.author = request.user
        comment.save()
    return redirect_url


@login_required
def comment_delete(request, **id):
    comment_id = id['comment_id']
    comment = get_object_or_404(Comment, pk=comment_id)
    redirect_url = get_redirect_url(id)
    if comment.author != request.user:
        return redirect_url
    comment.delete()
    return redirect_url


@login_required
def comment_edit(request, **id):
    comment_id = id['comment_id']
    comment = get_object_or_404(Comment, pk=comment_id)
    redirect_url = get_redirect_url(id)
    if comment.author != request.user:
        return redirect_url
    form = CommentForm(request.POST or None, instance=comment)
    if form.is_valid():
        form.save()
        return redirect_url
    context = {
        'form': form,
        'comment': comment,
    }
    return render(request, 'counterparties/comment_edit.html', context)
