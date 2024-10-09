from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = (
        'email',
        'first_name',
        'middle_name',
        'last_name',
        'letter_of_attorney',
        'post',
        'birth_date',
        'photo',
        'is_staff',
        'is_active',
    )
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email',
                           'password',
                           'first_name',
                           'middle_name',
                           'last_name',
                           'letter_of_attorney',
                           'post',
                           'birth_date',
                           'photo',)}),
        ('Разрешения', {'fields': ('is_staff', 'is_active', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email',
                       'password1',
                       'password2',
                       'first_name',
                       'middle_name',
                       'last_name',
                       'letter_of_attorney',
                       'post',
                       'birth_date',
                       'is_staff',
                       'is_active',
                       'groups',
                       'user_permissions'
            )}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
