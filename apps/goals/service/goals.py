from django.db.models import Sum, Q

from apps.accounts.service.accounts import get_current_account
from apps.goals.models import Goal
from apps.transactions.models import Transaction
from components.header.set_month import get_current_date


def get_goals(request):
    if not request.user.is_authenticated:
        return Goal.objects.none()
    account = get_current_account(request)
    return Goal.objects.filter(account=account)


def add_total_expenses(goals):
    return goals.annotate(
        total_expenses=Sum('transactions__amount', filter=Q(transactions__type=Transaction.TransactionType.EXPENSE)))


def deposit_on_period(request, goals):
    d_from, d_to = get_current_date(request)
    return goals.aggregate(
        period_total_expenses=Sum('transactions__amount',
                                  filter=Q(transactions__type=Transaction.TransactionType.EXPENSE,
                                           transactions__date__gte=d_from,
                                           transactions__date__lte=d_to)))['period_total_expenses'] or 0
