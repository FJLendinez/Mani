from dateutil.utils import today
from django import forms
from django_components import component

from apps.accounts.models import Account
from apps.accounts.service.accounts import get_current_account, get_accounts
from apps.core.form_views import HTMXFormView
from apps.core.utils import client_redirect
from apps.transactions.models import Transaction


class TransferForm(forms.Form):
    original_account = forms.ModelChoiceField(queryset=Account.objects.none(), required=False,
                                              widget=forms.Select(attrs={'class': 'form-control hidden'}))
    destination_account = forms.ModelChoiceField(label='Cuenta destino', queryset=Account.objects.none(),
                                                 widget=forms.Select(attrs={'class': 'form-control input input-sm input-bordered input-accent w-full '}))
    amount = forms.DecimalField(label='Cantidad', max_digits=10, decimal_places=2,
                                widget=forms.NumberInput(attrs={'class': 'form-control input input-sm input-bordered input-accent w-full '}))

    def __init__(self, request, *args, **kwargs):
        super(TransferForm, self).__init__(*args, **kwargs)
        self.request = request
        user_accounts = get_accounts(request)
        self.current_account = self.clean_original_account()
        self.fields['original_account'].queryset = user_accounts
        self.fields['destination_account'].queryset = user_accounts.exclude(id=self.current_account.id)

    def clean_original_account(self):
        account = get_current_account(self.request)
        if not account:
            raise forms.ValidationError('No se ha detectado cuenta en uso')
        return account


@component.register('transfer')
class TransferComponent(HTMXFormView, component.Component):
    modal_title = 'Transferir'
    modal_button = 'Transferir'
    action_url = 'transfer'
    form_class = TransferForm

    def form_valid(self, form):
        Transaction.objects.create(account=form.cleaned_data['original_account'],
                                   type=Transaction.TransactionType.EXPENSE,
                                   amount=form.cleaned_data['amount'],
                                   description=f'Trans. a cuenta {form.cleaned_data["destination_account"].name}.',
                                   date=today())
        Transaction.objects.create(account=form.cleaned_data['destination_account'],
                                   type=Transaction.TransactionType.INCOME,
                                   amount=form.cleaned_data['amount'],
                                   description=f'Trans. desde cuenta {form.cleaned_data["original_account"].name}.',
                                   date=today())
        return client_redirect('/transactions/')
