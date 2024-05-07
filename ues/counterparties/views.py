from django.shortcuts import get_object_or_404, redirect, render

from .forms import CounterpartyForm


from .models import Counterparty


def index(request):
    counterparties = Counterparty.objects.all()
    context = {
        'counterparties': counterparties,
    }
    return render(request, 'counterparties/index.html', context)


def counterparty_create(request):
    form = CounterpartyForm(request.POST or None)
    if form.is_valid():
        counterparty = form.save(commit=False)
        counterparty.save()
        return redirect('counterparties.counterparty.id')
    context = {
        'form': form,
    }
    return render(request, 'counterparties/counterparty_create.html', context)


def counterparty_detail(request, counterparty_id):
    counterparty = get_object_or_404(Counterparty, pk=counterparty_id)
    context = {
        'counterparty': counterparty,
    }
    return render(request, 'counterparties/counterperty_detail.html', context)
