# Generated by Django 4.2.11 on 2024-07-03 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('counterparties', '0004_contract_actual_cost_contract_сompletion_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='actual_cost',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Фактическая стоимость выполненных работ'),
        ),
    ]
