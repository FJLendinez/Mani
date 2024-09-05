from dateutil.utils import today
from django import forms
from django_components import component

from apps.accounts.models import Account
from apps.accounts.service.accounts import get_current_account, get_accounts
from apps.core.form_views import HTMXFormView
from apps.core.utils import client_redirect
from apps.goals.models import Goal
from apps.transactions.models import Transaction


class DepositForm(forms.Form):
    account = forms.ModelChoiceField(queryset=Account.objects.none(), required=False,
                                     widget=forms.Select(attrs={'class': 'form-control hidden'}))
    goal = forms.ModelChoiceField(label='Objetivo', queryset=Goal.objects.all(),
                                  widget=forms.Select(attrs={'class': 'form-control input input-sm input-bordered input-accent w-full'}))
    amount = forms.DecimalField(label='Cantidad', max_digits=10, decimal_places=2,
                                widget=forms.NumberInput(attrs={'class': 'form-control input input-sm input-bordered input-accent w-full'}))

    def __init__(self, request, *args, **kwargs):
        super(DepositForm, self).__init__(*args, **kwargs)
        self.request = request
        self.fields['account'].queryset = get_accounts(self.request)
        self.fields['goal'].queryset = Goal.objects.filter(account__in=self.fields['account'].queryset)

    def clean_account(self):
        account = get_current_account(self.request)
        if not account:
            raise forms.ValidationError('No se ha detectado cuenta en uso')
        return account


class DepositComponent(HTMXFormView, component.Component):
    action_url = 'deposit'
    modal_title = 'Depositar'
    modal_button = 'Depositar'
    form_class = DepositForm

    def form_valid(self, form):
        Transaction.objects.create(account=form.cleaned_data['account'],
                                   type=Transaction.TransactionType.EXPENSE,
                                   amount=form.cleaned_data['amount'],
                                   description=f'Depósito para {form.cleaned_data["goal"].name}.',
                                   goal=form.cleaned_data['goal'],
                                   date=today())
        return client_redirect('.')
