from django import forms
from django_components import component

from apps.accounts.models import Account
from apps.accounts.service.accounts import get_current_account
from apps.core.form_views import HTMXFormView, HTMXObjectFormView, HTMXDeleteFormView
from apps.debts.models import Debt


class DebtForm(forms.ModelForm):
    account = forms.ModelChoiceField(queryset=Account.objects.none(), required=False,
                                     widget=forms.Select(attrs={'class': 'form-control hidden'}))

    class Meta:
        model = Debt
        fields = '__all__'

    def __init__(self, request, *args, **kwargs):
        super(DebtForm, self).__init__(*args, **kwargs)
        self.request = request
        for f in self.fields:
            self.fields[f].widget.attrs = {
                **{'class': 'form-control input input-sm input-bordered input-accent w-full'},
                **(self.fields[f].widget.attrs or {})}

    def clean_account(self):
        account = get_current_account(self.request)
        if not account:
            raise forms.ValidationError('No se ha detectado cuenta en uso')
        return account


class DebtFormComponent(HTMXFormView, component.Component):
    form_class = DebtForm
    success_url = '.'
    action_url = 'debt-form'


class DebtUpdateFormComponent(HTMXObjectFormView, component.Component):
    queryset = Debt.objects.none()
    form_class = DebtForm
    success_url = '.'
    action_url = 'debt-update-form'

    def get_queryset(self):
        current_account = get_current_account(self.request)
        return Debt.objects.filter(account=current_account)


class DebtDeleteFormComponent(HTMXDeleteFormView, component.Component):
    success_url = '.'
    action_url = 'debt-delete-form'

    def get_queryset(self):
        current_account = get_current_account(self.request)
        return Debt.objects.filter(account=current_account)

    def form_valid(self, form):
        from apps.core.utils import client_redirect
        success_url = self.get_success_url()
        self.object.archived = True
        self.object.save()
        return client_redirect(success_url)
