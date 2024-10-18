from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models


User = get_user_model()


def contract_directory_path(instance, filename):
    return 'contracts/contract_{0}/{1}'.format(instance.contract.title, filename)


class Comment(models.Model):
    """A class model for creating comments on counterparties,
    contracts and accounting points.
    """
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор комментария',
    )
    text = models.TextField('Комментарий')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
    )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey(
        'content_type',
        'object_id',
    )

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Коментирии'

    def __str__(self) -> str:
        return self.text[:20]


class Document(models.Model):
    contract = models.ForeignKey(
        'Contract',
        on_delete=models.CASCADE,
        related_name='documents',
    )
    conclusion_date = models.DateField(
        'Дата подписания документа',
        auto_now=False,
        auto_now_add=False,
        null=True,
        blank=True,
    )
    title = models.CharField(
        'Наименование документа',
        max_length=255,
    )
    file = models.FileField(
        upload_to=contract_directory_path,
    )

    def __str__(self) -> str:
        return self.title
    
    class Meta:
        verbose_name = 'Документ'
        verbose_name_plural = 'Документы'
        ordering = ('conclusion_date',)


class Contract(models.Model):
    comment = GenericRelation(Comment, related_query_name='contract')
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
        null=True,
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
    comment = GenericRelation(Comment, related_query_name='counterparty')
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
        ordering = ('full_name',)
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'

    def __str__(self) -> str:
        return self.short_name
