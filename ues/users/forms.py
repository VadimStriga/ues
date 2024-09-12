from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUser


class BirthDateInput(forms.DateInput):
    input_type = "date"
    format = "%Y-%m-%d"


class CustomUserCreationForm(UserCreationForm):
    birth_date = forms.DateField(
        label="Дата рождения",
        required=True,
        widget=BirthDateInput({"class": "form-control"})
    )

    class Meta:
        model = CustomUser
        fields = (
            "first_name",
            "middle_name",
            "last_name",
            "email",
            "post",
            "birth_date",
            "photo",
        )


class CustomUserChangeForm(UserChangeForm):
    birth_date = forms.DateField(
        label="Дата рождения",
        required=True,
        widget = BirthDateInput({"class": "form-control"}),
        localize=True,
    )

    class Meta:
        model = CustomUser
        fields = (
            "email",
            "first_name",
            "middle_name",
            "last_name",
            "post",
            "birth_date",
            "photo",
        )
