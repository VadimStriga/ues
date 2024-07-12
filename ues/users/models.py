from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    """User model."""
    username = None
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(
        'Имя',
        max_length=254,
        blank=False,
    )
    middle_name = models.CharField(
        'Отчество',
        max_length=254,
        blank=True,
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=254,
        blank=False,
    )
    post = models.CharField(
        'Должность',
        max_length=254,
        blank=False,
    )
    photo = models.ImageField(
        'Фотография сотрудника',
        upload_to='users/photo/',
        blank=True,
    )
    birth_date = models.DateField(
        'Дата рождения',
        auto_now=False,
        auto_now_add=False,
        null=True,
        blank=True,
    )


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = ('Сотрудник организации')
        verbose_name_plural = ('Сотрудники организации')

        def __str__(self):
            return self.email
