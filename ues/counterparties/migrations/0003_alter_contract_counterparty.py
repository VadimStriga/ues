# Generated by Django 4.2.11 on 2024-07-03 07:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('counterparties', '0002_contract'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='counterparty',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contracts', to='counterparties.counterparty'),
        ),
    ]
