from django.contrib.contenttypes.fields import GenericRelation
from django.db import models

from counterparties.models import Comment, Contract


NDS = 20


def point_directory_path(instance, filename):
    return 'contracts/contract_{0}/points/point_{1}/{2}'.format(instance.point.contract.title, instance.point.name, filename)


def meter_directory_path(instance, filename):
    return 'contracts/contract_{0}/points/point_{1}/{2}'.format(instance.meter.point.contract.title, instance.meter.point.name, filename)


class Document(models.Model):
    point = models.ForeignKey(
        'ElectricityMeteringPoint',
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
        upload_to=point_directory_path,
    )

    def __str__(self) -> str:
        return self.title
    
    class Meta:
        verbose_name = 'Документ'
        verbose_name_plural = 'Документы'
        ordering = ('conclusion_date',)


class ElectricityMeteringPoint(models.Model):
    """Class for creating a model of an electricity metering point."""
    TARIFF_CHOICES = [
        ('urban_tariff', 'Тариф для городского населения с однотирфным прибором учета'),
        ('rural_tariff', 'Тариф для сельского населения с однотирфным прибором учета'),
        ('low_voltage_tariff', 'Тариф для потребителей с уровнем напряжения НН, рассчитывающихся по I ценовой категории'),
        ('medium_voltage_tariff_1', 'Тариф для потребителей с уровнем напряжения СН-I, рассчитывающихся по I ценовой категории'),
        ('medium_voltage_tariff_2', 'Тариф для потребителей с уровнем напряжения СН-II, рассчитывающихся по I ценовой категории'),
        ('high_voltage_tariff', 'Тариф для потребителей с уровнем напряжения ВН, рассчитывающихся по I ценовой категории'),
        ('tariff-free', 'Бездоговорное потребление'),
    ]
    TYPE_OF_ACCOUNTING = [
        ('Calculation accounting', 'Расчётный учёт'),
        ('Control accounting', 'Контрольный учёт'),
        ('Mutual settlement accounting', 'Взаиморасчетный учёт'),
        ('Transit accounting', 'Транзитный учёт'),
    ]
    comment = GenericRelation(Comment, related_query_name='point')
    constant_losses = models.PositiveIntegerField(
        'Постоянныен потери трансформатора, кВтч/месяц'
    )
    contract = models.ForeignKey(
        Contract,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='Договор',
        related_name='points',
    )
    name = models.CharField(
        'Наименование точки учёта',
        max_length=255,
    )
    location = models.CharField(
        'Место расположение точки учета',
        max_length=255,
        blank=True,
    )
    losses = models.FloatField(
        'Процент потерь на линиях'
    )
    margin = models.FloatField(
        'Наценка',
        help_text='Добавочная стоимость, руб./кВтч'
    )
    power_supply = models.CharField(
        'Источник питания',
        max_length=255,
    )
    tariff = models.CharField(
        'Тариф',
        max_length=200,
        choices=TARIFF_CHOICES,
        default='tariff-free',
    )
    transformation_coefficient = models.PositiveIntegerField(
        'Коэффициент транформации',
        help_text='''Отношение напряжений на зажимах двух обмоток в режиме холостого
                     хода, принимается равным отношению чисел их витков.'''
    )
    type_of_accounting = models.CharField(
        'Тип учёта',
        max_length=255,
        choices=TYPE_OF_ACCOUNTING,
        default='Calculation accounting',
        help_text=('Прибор учёта может быть расчетным, контрольным, '
                   'взаиморасчетным, транзитным. Для взаиморасчетных приборов '
                   'указывается из-под какого (№ счетчика) производится расчет')
    )

    class Meta:
        verbose_name = 'Точка учета электроэнергии'
        verbose_name_plural = 'Точки учета электроэнергии'
        ordering=('contract',)

    def __str__(self) -> str:
        return self.name


class ElectricityMeter(models.Model):
    """Model for creating electric energy meters.
    Electric energy meters are part of electricity metering points.
    """
    is_active = models.BooleanField(
        default=True,
        verbose_name='Статус',    
    )
    mark = models.CharField(
        'Марка счётчика электроэнергии',
        max_length=255,
        blank=True,
    )
    number = models.CharField(
        'Заводской номер счётчика электроэнергии',
        max_length=255,
        blank=True,
    )
    installation_date = models.DateField(
        'Дата установки',
    )
    date_of_next_verification = models.DateField(
        'Дата следующей поверки',
    )
    point = models.ForeignKey(
        'ElectricityMeteringPoint',
        on_delete=models.CASCADE,
        default=None,
        verbose_name='Точка учёта электроэнергии',
        related_name='meters',
    )
    photo = models.ImageField(
        'Фотография счётчика',
        upload_to='contracts/',
        blank=True,
    )

    class Meta:
        verbose_name = 'Счётчик электроэнергии'
        verbose_name_plural = 'Счётчики электроэнергии'
        ordering=('-installation_date',)
    
    def __str__(self) -> str:
        return self.number


class CurrentTransformer(models.Model):
    """Model for creating current transformers.
    Current transformers are part of electricity metering points.
    """
    is_active = models.BooleanField(
        default=True,
        verbose_name='Статус',
    )
    mark = models.CharField(
        'Тип трансформатора тока',
        max_length=255,
        blank=True,
    )
    number = models.CharField(
        'Заводской номер трансформатора тока',
        max_length=255,
        blank=True,
    )
    installation_date = models.DateField(
        'Дата установки',
    )
    date_of_next_verification = models.DateField(
        'Дата следующей поверки',
    )
    point = models.ForeignKey(
        'ElectricityMeteringPoint',
        on_delete=models.CASCADE,
        default=None,
        verbose_name='Точка учёта электроэнергии',
        related_name='transformers',
    )
    photo = models.ImageField(
        'Фотография трансформатора тока',
        upload_to=point_directory_path,
        blank=True,
    )

    class Meta:
        verbose_name = 'Трансформатор тока'
        verbose_name_plural = 'Трансформаторы тока'
    
    def __str__(self) -> str:
        return self.number


class Tariff(models.Model):
    """Model for entering tariffs for electricity."""
    pub_date = models.DateField(
        'Дата внесения расценок',
        auto_now_add=True,
    )
    begin_tariff_period = models.DateField(
        'Начало периода',
        help_text='Начало периода действия тарифов',
        auto_now=False,
        auto_now_add=False,
    )
    end_tariff_period = models.DateField(
        'Окончание периода',
        help_text='Окончание периода действия тарифов',
        auto_now=False,
        auto_now_add=False,
    )
    urban_tariff_1 = models.FloatField(
        'Городское 1',
        help_text='''Тариф для городского населения с однотирфным прибором учета.
                     Для первого диапазона объемов потребления (до 10980 кВт*ч)''',
    )
    urban_tariff_2 = models.FloatField(
        'Городское 2',
        help_text='''Тариф для городского населения с однотирфным прибором учета.
                     Для второго диапазона объемов потребления (от 10980 – 14640 кВт*ч)''',
    )
    urban_tariff_3 = models.FloatField(
        'Городское 3',
        help_text='''Тариф для городского населения с однотирфным прибором учета.
                     Для третьего диапазона объемов потребления (свыше 14640 кВт*ч)''',
    )
    rural_tariff_1 = models.FloatField(
        'Сельское 1',
        help_text='''Тариф для сельского населения с однотирфным прибором учета.
                     Для первого диапазона объемов потребления (до 10980 кВт*ч)''',
    )
    rural_tariff_2 = models.FloatField(
        'Сельское 2',
        help_text='''Тариф для сельского населения с однотирфным прибором учета.
                     Для второго диапазона объемов потребления (от 10980 – 14640 кВт*ч)''',
    )
    rural_tariff_3 = models.FloatField(
        'Сельское 3',
        help_text='''Тариф для сельского населения с однотирфным прибором учета.
                     Для третьего диапазона объемов потребления (свыше 14640 кВт*ч)''',
    )
    high_voltage_tariff = models.FloatField(
        'ВН',
        help_text='''Тариф для потребителей с уровнем напряжения ВН,
                     рассчитывающихся по I ценовой категории''',
    )
    medium_voltage_tariff_1 = models.FloatField(
        'СН-I',
        help_text='''Тариф для потребителей с уровнем напряжения СН-I,
                     рассчитывающихся по I ценовой категории''',
    )
    medium_voltage_tariff_2 = models.FloatField(
        'СН-II',
        help_text='''Тариф для потребителей с уровнем напряжения СН-II,
                     рассчитывающихся по I ценовой категории''',
    )
    low_voltage_tariff = models.FloatField(
        'НН',
        help_text='''Тариф для потребителей с уровнем напряжения НН,
                     рассчитывающихся по I ценовой категории''',
    )
    

    class Meta:
        verbose_name = 'Тариф'
        verbose_name_plural = 'Тарифы'
        ordering = ('-end_tariff_period',)


class Calculation(models.Model):
    """The model for calculating the amount of electricity consumed and for
    calculating the cost of this volume.
    """
    point = models.ForeignKey(
        ElectricityMeteringPoint,
        on_delete=models.CASCADE,
        related_name='calculations'
    )
    meter = models.ForeignKey(
        ElectricityMeter,
        on_delete=models.CASCADE,
    )
    entry_date = models.DateField(
        'Дата снятия показаний',
        auto_now=False,
        auto_now_add=False,
    )
    readings = models.FloatField('Показания счётчика электрической энергии',)
    previous_entry_date = models.DateField(
        'Дата снятия предыдущих показаний',
        auto_now=False,
        auto_now_add=False,
    )
    previous_readings = models.FloatField('Предыдущие показания счётчика электрической энергии',)
    difference_readings = models.FloatField('Разность показаний',)
    transformation_coefficient = models.PositiveIntegerField('Коэффициент транформации',)
    amount = models.FloatField('Количество кВтч',)
    deductible_amount = models.FloatField('Вычитаемое количество кВтч',)
    losses = models.FloatField('Процент потерь на линиях')
    constant_losses = models.PositiveIntegerField('Постоянныен потери трансформатора, кВтч/месяц')
    result_amount = models.FloatField('Результат кВтч',)
    tariff1 = models.FloatField(
        'Тариф для первого диапазона объёмов потребления (до 10980 кВт*ч)',
    )
    tariff2 = models.FloatField(
        'Тариф для второго диапазона объёмов потребления (от 10980 – 14640 кВт*ч)',
    )
    tariff3 = models.FloatField(
        'Тариф тля третьего диапазона объёмов потребления (свыше 14640 кВт*ч)',
    )
    margin = models.FloatField(
        'Наценка',
        help_text='Добавочная стоимость, руб./кВтч'
    )
    accrued = models.FloatField('Начислено',)
    accrued_NDS = models.FloatField('Начислено с НДС',)

    class Meta:
        verbose_name = 'Показания'
        verbose_name_plural = 'Показания'
        ordering = ('-entry_date',)


class InterconnectedPoints(models.Model):
    """The model for creating links between accounting points.
    It is required to deduct the amount of electricity consumed by the
    counterparty from the volume recorded in the higher-level metering device.
    """
    head_point = models.ForeignKey(
        ElectricityMeteringPoint,
        on_delete=models.CASCADE,
        verbose_name='Головной учёт',
        related_name='head_point',
    )
    lower_point = models.ForeignKey(
        ElectricityMeteringPoint,
        on_delete=models.CASCADE,
        verbose_name='Нижестоящий учёт',
        related_name='lower_point',
        help_text=('Выберите нижестоящую точку учёта. Объём потребленной',
                   'электроэнрегии выбранной нижестоящей точки учета',
                   'будет вычитаться из объёма потреблённой электроэнергии',
                   'вышестоящей точки учёта.'),
    )

    class Meta:
        verbose_name = 'Взаимосвязь'
        verbose_name_plural = 'Взаимосвязи'
        constraints = [
            models.UniqueConstraint(
                fields=['head_point', 'lower_point'],
                name='unique_deduction',
            )
        ]
