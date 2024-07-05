from django.db import models


class Contract(models.Model):
    counterparty = models.ForeignKey(
        'Counterparty',
        on_delete=models.CASCADE,
        related_name='contracts',
    )
    title = models.CharField(
        'Номер договора',
        max_length=255,
    )
    conclusion_date = models.DateField(
        'Дата заключения договора',
        auto_now=False,
        auto_now_add=False,
        null=True,
        blank=True,
    )
    contract_price = models.PositiveIntegerField(
        'Цена договора',
        blank=True,
    )
    purchase_code = models.CharField(
        'Идентификационный код закупки',
        max_length=255,
        blank=True,
        help_text=(
            'Если договор заключен конкурентным способом, введите'
            ' идентификационный код закупки с сайта https://zakupki.gov.ru'
        ),
    )
    description = models.TextField(
        'Объект закупки',
        help_text='Введите описание работ',
    )
    сompletion_date = models.DateField(
        'Дата завершения работ',
        auto_now=False,
        auto_now_add=False,
        blank=True,
        null=True,
    )
    actual_cost = models.PositiveIntegerField(
        'Фактическая стоимость выполненных работ',
        blank=True,
        null=True,
    )


    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Договор'
        verbose_name_plural = 'Договоры'
        ordering = ('conclusion_date',)


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
