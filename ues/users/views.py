from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models.base import Model as Model
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import CreateView
from django.urls import reverse_lazy

from .forms import CustomUserCreationForm, CustomUserChangeForm


User = get_user_model()


NUMBER_OF_OUTPUT_PROFILES = 25


class SignUp(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'users/signup.html'


@login_required
def user_edit(request):
    user_id=request.user.id
    print(user_id)
    if request.method == 'POST':
        print(f'request.method == POST')
        form = CustomUserChangeForm(request.POST, files=request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            print(f'user_id {user_id}')
            return redirect(
                'users:user_profile',
                user_id,
            )
    else:
        form = CustomUserChangeForm(instance=request.user)
        context = {
            'form': form,
            'is_edit': True,
        }
    return render(request, 'users/user_edit.html', context)


def user_profile(request, user_id):
    profile = get_object_or_404(User, pk=user_id)
    context = {
        'profile': profile, 
    }
    return render(request, 'users/user_detail.html', context)


def users_list(request):
    profiles = User.objects.filter(is_active=True).order_by('last_name')
    paginator = Paginator(profiles, NUMBER_OF_OUTPUT_PROFILES)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    users_count = User.objects.filter(is_active=True).count()
    context = {
        'page_obj': page_obj,
        'users_count': users_count,
    }
    return render(request, 'users/users_list.html', context)
