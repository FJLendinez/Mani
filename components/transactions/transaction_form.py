from django import forms
from django_components import component
from webpush import send_user_notification

from apps.accounts.models import Account
from apps.accounts.service.accounts import get_accounts, get_current_account
from apps.core.fields import DateField
from apps.core.form_views import HTMXFormView, HTMXObjectFormView, HTMXDeleteFormView
from apps.debts.models import Debt
from apps.transactions.models import Transaction, Category


class TransactionForm(forms.ModelForm):
    account = forms.ModelChoiceField(queryset=Account.objects.none(), required=False,
                                     widget=forms.Select(attrs={
                                         'class': 'form-control input input-sm input-bordered input-accent w-full  hidden'}))
    description = forms.CharField(label='Concepto', widget=forms.TextInput(
        attrs={'class': 'form-control input input-sm input-bordered input-accent w-full '}))
    amount = forms.DecimalField(label='Cantidad', max_digits=10, decimal_places=2,
                                widget=forms.NumberInput(
                                    attrs={'class': 'form-control input input-sm input-bordered input-accent w-full '}))
    date = DateField(label='Fecha',
                     widget=forms.DateInput(
                         attrs={'class': 'form-control input input-sm input-bordered input-accent w-full '}))
    type = forms.ChoiceField(label='Tipo', choices=Transaction.TransactionType.choices,
                             initial=Transaction.TransactionType.EXPENSE,
                             widget=forms.Select(
                                 attrs={'class': 'form-control input input-sm input-bordered input-accent w-full '}))
    category = forms.ModelChoiceField(label='Categoría', queryset=Category.objects.all(),
                                      widget=forms.Select(attrs={
                                          'class': 'form-control input input-sm input-bordered input-accent w-full '}),
                                      required=False)
    debt = forms.ModelChoiceField(label='Deuda', queryset=Debt.objects.filter(archived=False),
                                  widget=forms.Select(attrs={
                                      'class': 'form-control input input-sm input-bordered input-accent w-full '}),
                                  required=False)

    class Meta:
        model = Transaction
        fields = [
            "account",
            "description",
            "amount",
            "date",
            "type",
            "category",
            "debt"]

    def __init__(self, request, *args, **kwargs):
        super(TransactionForm, self).__init__(*args, **kwargs)
        self.request = request
        user_accounts = get_accounts(request)
        self.fields['account'].queryset = user_accounts
        self.fields['category'].queryset = Category.objects.filter(account=get_current_account(self.request))
        self.fields['debt'].queryset = Debt.objects.filter(account=get_current_account(self.request), archived=False)
        if self.initial.get('date'):
            self.initial['date'] = self.initial['date'].isoformat()
        if self.is_bound:
            self.data = self.data.copy()
            self.data['account'] = get_current_account(self.request)

    def save(self, commit=True):
        transaction = super().save(commit=commit)
        if not self.instance:
            payload = {"head": "Nuevo movimiento!",
                       "body": f"{self.request.user.username} ha realizado un movimiento de {transaction.amount}€ en {transaction.account.name} con concepto {transaction.description}"}
            for user in transaction.account.users.all().exclude(id=self.request.user.id):
                print(f"Sending notification to {user.username}. Payload: {payload}")
                send_user_notification(user=user, payload=payload, ttl=1000)


class TransactionFormComponent(HTMXFormView, component.Component):
    action_url = 'transaction-form'
    success_url = '.'
    form_class = TransactionForm
    modal_title = "Nuevo movimiento"


class TransactionUpdateFormComponent(HTMXObjectFormView, component.Component):
    queryset = Transaction.objects.none()
    form_class = TransactionForm
    success_url = '.'
    action_url = 'transaction-update-form'

    def get_queryset(self):
        current_account = get_current_account(self.request)
        return Transaction.objects.filter(account=current_account)


class TransactionDeleteFormComponent(HTMXDeleteFormView, component.Component):
    success_url = '.'
    action_url = 'transaction-delete-form'

    def get_queryset(self):
        current_account = get_current_account(self.request)
        return Transaction.objects.filter(account=current_account)
