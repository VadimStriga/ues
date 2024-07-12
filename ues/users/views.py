from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, render
from django.views.generic import CreateView
from django.urls import reverse_lazy

from .forms import CustomUserCreationForm


User = get_user_model()


class SignUp(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("counterparties:index")
    template_name = "users/signup.html"


def user_profile(request, user_id):
    profile = get_object_or_404(User, pk=user_id)
    context = {
        "profile": profile, 
    }
    return render(request, "users/profile.html", context)
