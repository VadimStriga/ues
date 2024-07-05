# Generated by Django 4.2.11 on 2024-07-02 02:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('counterparties', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Номер договора')),
                ('conclusion_date', models.DateField(blank=True, null=True, verbose_name='Дата заключения договора')),
                ('contract_price', models.PositiveIntegerField(blank=True, verbose_name='Цена договора')),
                ('purchase_code', models.CharField(blank=True, help_text='Если договор заключен конкурентным способом, введите идентификационный код закупки с сайта https://zakupki.gov.ru', max_length=255, verbose_name='Идентификационный код закупки')),
                ('description', models.TextField(help_text='Введите описание работ', verbose_name='Объект закупки')),
                ('counterparty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='counterparties.counterparty')),
            ],
            options={
                'verbose_name': 'Договор',
                'verbose_name_plural': 'Договоры',
                'ordering': ('conclusion_date',),
            },
        ),
    ]
