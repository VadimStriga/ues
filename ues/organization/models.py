from django.db import models


class Organization(models.Model):
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
        help_text='''ОГРН - основной государственный регистрационный номер.
                     ОГРН состоит из 13 арабских цифр.
                     ОГРН индивидуального предпринимателя (ОГРНИП) состоит
                     из 15 арабских цифр.'''
    )
    tax_identification_number = models.PositiveBigIntegerField(
        'ИНН',
        db_column='INN',
        unique=True,
        help_text='''ИНН — идентификационный номер налогоплательщика. 
                     ИНН физического лица состоит из 12 арабских цифр. 
                     ИНН юридического лица состоит из 10 арабских цифр.'''
    )
    registration_reason_code = models.PositiveIntegerField(
        'КПП',
        db_column='KPP',
        blank=True,
        null=True,
        help_text='''КПП - код причины постановки на учёт.
                     КПП юридического лица состоит из 9 арабских цифр.
                     Индивидуальные предприниматели не имеют КПП
                     (приказ ФНС №ММВ-7-6/435).'''
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
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'

    def __str__(self) -> str:
        return self.short_name
    
    def save(self, *args, **kwargs):
        if self.__class__.objects.count():
            self.pk = self.__class__.objects.first().pk
        super().save(*args, **kwargs)
