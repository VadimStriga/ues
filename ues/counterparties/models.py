from django.db import models


class Counterparty(models.Model):
    full_name = models.CharField(
        'Полное наименование',
        max_length=255,
    )
    short_name = models.CharField(
        'Сокращенное наименование',
        max_length=255,
    )
    address = models.CharField(
        'Юридический адрес',
        max_length=200,
    )
    phone_number = models.CharField(
        'Номер телефона',
        blank=True,
        max_length=16,
    )
    email = models.EmailField(
        'Электронный адрес',
        blank=True,
    )
    main_state_registration_number = models.PositiveBigIntegerField(
        'ОГРН',
        db_column='OGRN',
        unique=True,
    )
    registration_reason_code = models.PositiveIntegerField(
        'КПП',
        db_column='KPP',
    )
    tax_identification_number = models.PositiveBigIntegerField(
        'ИНН',
        db_column='INN',
        unique=True,
    )
    job_title = models.CharField(
        'Должность руководителя',
        blank=True,
        max_length=200,
    )
    person_full_name = models.CharField(
        'Фамилия, имя и отчество (если есть)',
        max_length=200,
    )

    class Meta:
        ordering = ('full_name',)
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'

    def __str__(self) -> str:
        return self.short_name
