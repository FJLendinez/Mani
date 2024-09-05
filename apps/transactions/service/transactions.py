from datetime import datetime

from apps.accounts.service.accounts import get_current_account
from apps.transactions.models import Transaction
from components.header.set_month import get_current_date


def get_transactions(user):
    if not user:
        return Transaction.objects.none()
    return Transaction.objects.filter(account__users=user).order_by('-id')


def get_current_date_range_transactions(request):
    d_from, d_to = get_current_date(request)
    return get_transactions(user=request.user).filter(date__gte=d_from, date__lte=d_to)


def get_current_account_transactions(request):
    acc = get_current_account(request)
    return Transaction.objects.filter(account=acc)


def filter_current_account_transactions(request, transactions):
    acc = get_current_account(request)
    return transactions.filter(account=acc)


def get_current_transactions(request):
    transactions = get_current_date_range_transactions(request)
    return filter_current_account_transactions(request, transactions)
