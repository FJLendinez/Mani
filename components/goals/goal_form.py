from django import forms
from django_components import component

from apps.accounts.models import Account
from apps.accounts.service.accounts import get_current_account
from apps.core.fields import DateField
from apps.core.form_views import HTMXFormView, HTMXObjectFormView, HTMXDeleteFormView
from apps.goals.models import Goal


class GoalForm(forms.ModelForm):
    account = forms.ModelChoiceField(queryset=Account.objects.none(), required=False,
                                     widget=forms.Select(attrs={'class': 'form-control hidden'}))
    date = DateField(label='Fecha', widget=forms.DateInput(attrs={'class': 'form-control input input-sm input-bordered input-accent w-full'}))
    description = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control input input-sm input-bordered input-accent w-full'}),
                                  required=False)

    class Meta:
        model = Goal
        fields = '__all__'
        labels = {
            "name": "Objetivo",
            "description": "Descripción",
            "amount": "Cantidad"
        }

    def __init__(self, request, *args, **kwargs):
        super(GoalForm, self).__init__(*args, **kwargs)
        self.request = request
        for f in self.fields:
            self.fields[f].widget.attrs = {**{'class': 'form-control input input-sm input-bordered input-accent w-full'},
                                           **(self.fields[f].widget.attrs or {})}

    def clean_account(self):
        account = get_current_account(self.request)
        if not account:
            raise forms.ValidationError('No se ha detectado cuenta en uso')
        return account


class GoalFormComponent(HTMXFormView, component.Component):
    form_class = GoalForm
    success_url = '.'
    action_url = 'goal-form'


class GoalUpdateFormComponent(HTMXObjectFormView, component.Component):
    queryset = Goal.objects.none()
    form_class = GoalForm
    success_url = '.'
    action_url = 'goal-update-form'

    def get_queryset(self):
        current_account = get_current_account(self.request)
        return Goal.objects.filter(account=current_account)


class GoalDeleteFormComponent(HTMXDeleteFormView, component.Component):
    success_url = '.'
    action_url = 'goal-delete-form'

    def get_queryset(self):
        current_account = get_current_account(self.request)
        return Goal.objects.filter(account=current_account)
