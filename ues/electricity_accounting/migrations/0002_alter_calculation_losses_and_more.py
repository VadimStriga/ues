# Generated by Django 4.2.11 on 2024-11-18 02:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('electricity_accounting', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calculation',
            name='losses',
            field=models.FloatField(verbose_name='Процент потерь на линиях'),
        ),
        migrations.AlterField(
            model_name='currenttransformer',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Статус'),
        ),
        migrations.AlterField(
            model_name='electricitymeteringpoint',
            name='losses',
            field=models.FloatField(verbose_name='Процент потерь на линиях'),
        ),
    ]
