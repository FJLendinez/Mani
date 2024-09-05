from django.db import models
from django.db.models import Sum, OuterRef, Subquery, DecimalField

from apps.accounts.models import Account


class Debt(models.Model):
    class DebtType(models.TextChoices):
        LEND = 'LEND', 'Yo presto dinero'
        LOAN = 'LOAN', 'Me prestan dinero'

    account = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name='Cuenta')
    name = models.CharField(max_length=100, verbose_name='Nombre')
    type = models.CharField(max_length=4, choices=DebtType.choices, verbose_name='Tipo')
    archived = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name

    @staticmethod
    def aggregate_amount(queryset):
        from apps.transactions.models import Transaction

        transactions_income = Transaction.objects.filter(
            type=Transaction.TransactionType.INCOME, debt=OuterRef('pk')
        ).values('debt_id').order_by('debt_id').annotate(
            total_spend=Sum('amount')
        ).values(
            'total_spend'
        )
        transactions_expense = Transaction.objects.filter(
            type=Transaction.TransactionType.EXPENSE, debt=OuterRef('pk')
        ).values('debt_id').order_by('debt_id').annotate(
            total_spend=Sum('amount')
        ).values(
            'total_spend'
        )
        return queryset.annotate(transactions_income=Subquery(transactions_income, output_field=DecimalField()),
                                 transactions_expense=Subquery(transactions_expense, output_field=DecimalField()))
