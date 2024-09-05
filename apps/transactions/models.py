from django.db import models

from apps.accounts.models import Account
from apps.debts.models import Debt
from apps.goals.models import Goal


class Category(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name='Cuenta')
    name = models.CharField(max_length=100, verbose_name='Nombre')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Estimación mensual')

    def __str__(self):
        return self.name


class Transaction(models.Model):
    class TransactionType(models.TextChoices):
        INCOME = 'INCOME', 'Ingreso'
        EXPENSE = 'EXPENSE', 'Gasto'

    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    description = models.CharField(max_length=40)
    type = models.CharField(max_length=7, choices=TransactionType.choices, default=TransactionType.EXPENSE)
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL, blank=True, related_name='transactions')
    goal = models.ForeignKey(Goal, null=True, on_delete=models.SET_NULL, blank=True, related_name='transactions')
    debt = models.ForeignKey(Debt, null=True, on_delete=models.SET_NULL, blank=True, related_name='transactions')

    def __str__(self):
        return f"{self.amount} - {self.date} - {self.type} - {self.account}"
