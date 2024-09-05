from django.db.models import Sum

from apps.accounts.models import Account


def get_accounts(request):
    accounts = Account.objects.all()
    user = request.user
    if user.is_authenticated:
        accounts = accounts.filter(users=user)
        return accounts
    return accounts.none()


def set_current_account(request, account_id):
    user_accounts = get_accounts(request)
    if user_accounts.filter(id=account_id).exists():
        request.session['current_account'] = account_id
        return True
    return False


def get_current_account(request):
    user_accounts = get_accounts(request)
    if current_account_id := request.session.get('current_account'):
        return user_accounts.filter(id=current_account_id).first()

    default_account = user_accounts.first()
    if not default_account:
        return
    set_current_account(request, default_account.id)
    return default_account


def get_total_in_account(request):
    from apps.transactions.service.transactions import get_current_account_transactions
    transactions = get_current_account_transactions(request)
    from apps.transactions.models import Transaction
    expenses = transactions.filter(type=Transaction.TransactionType.EXPENSE).aggregate(Sum('amount'))['amount__sum'] or 0
    incomes = transactions.filter(type=Transaction.TransactionType.INCOME).aggregate(Sum('amount'))['amount__sum'] or 0
    return incomes - expenses
