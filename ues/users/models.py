from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(
        'Адрес электронной почты',
        max_length=254,
        blank=False,
        unique=True,
    )
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

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username',]

    class Meta:
        verbose_name = ('Сотрудник организации')
        verbose_name_plural = ('Сотрудники организации')

        def __str__(self):
            return self.username
