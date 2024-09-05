from django.db.models import Sum, Q, F

from apps.accounts.service.accounts import get_current_account
from apps.transactions.models import Category, Transaction
from components.header.set_month import get_current_date


def get_categories(request):
    if not request.user.is_authenticated:
        return Category.objects.none()
    acc = get_current_account(request)
    return Category.objects.filter(account=acc).order_by('-id')


def add_total_expenses(request, categories):
    periods = {'year': 12, 'month': 1, 'quarter': 3}
    period = request.session.get('period') or 'month'
    d_from, d_to = get_current_date(request)
    months = periods.get(period) or 1
    return categories.annotate(
        estimated=months * F('amount'),
        total_expenses=Sum('transactions__amount', filter=Q(transactions__type=Transaction.TransactionType.EXPENSE,
                                                            transactions__date__gte=d_from,
                                                            transactions__date__lte=d_to)))
