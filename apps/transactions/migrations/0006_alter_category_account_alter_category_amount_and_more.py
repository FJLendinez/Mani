# Generated by Django 5.0.8 on 2024-09-02 11:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_account_name'),
        ('transactions', '0005_transaction_debt'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='account',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.account', verbose_name='Cuenta'),
        ),
        migrations.AlterField(
            model_name='category',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Estimación mensual'),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Nombre'),
        ),
    ]
