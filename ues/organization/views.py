from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import TemplateView

from .forms import OrganizationForm
from .models import Organization


class IndexView(TemplateView):
    template_name = 'organization/about_organization.html'


@login_required
def organization_create(request):
    form = OrganizationForm(request.POST or None)
    if form.is_valid():
        organization = form.save(commit=False)
        organization.save()
        return redirect('organization:organization_detail')
    context = {
        'form': form,
    }
    return render(request, 'organization/organization_create.html', context)


@login_required
def organization_delete(request, organization_id):
    organization = get_object_or_404(Organization, pk=organization_id)
    organization.delete()
    return redirect('counterparties:index')


def organization_detail(request):
    organization = Organization.objects.first()
    context = {
        'organization': organization,
    }
    return render(request, 'organization/organization_detail.html', context)


@login_required
def organization_edit(request, organization_id):
    organization = get_object_or_404(Organization, pk=organization_id)
    form = OrganizationForm(request.POST or None, instance=organization)
    if form.is_valid():
        organization.save()
        return redirect('organization:organization_detail')
    context = {
        'form': form,
        'organization': organization,
        'is_edit': True,
    }
    return render(request, 'organization/organization_create.html', context)
