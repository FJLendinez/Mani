from django import forms
from django.views.generic.edit import BaseDeleteView
from django_components import component

from apps.accounts.models import Account
from apps.accounts.service.accounts import get_current_account
from apps.core.form_views import HTMXFormView, HTMXObjectFormView, HTMXDeleteFormView
from apps.core.utils import client_redirect
from apps.transactions.models import Category


class CategoryForm(forms.ModelForm):
    account = forms.ModelChoiceField(queryset=Account.objects.none(), required=False,
                                     widget=forms.Select(attrs={'class': 'form-control hidden'}))

    class Meta:
        model = Category
        fields = '__all__'

    def __init__(self, request, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        self.request = request
        for f in self.fields:
            self.fields[f].widget.attrs = {**{'class': 'form-control input input-sm input-bordered input-accent w-full'},
                                           **(self.fields[f].widget.attrs or {})}

    def clean_account(self):
        account = get_current_account(self.request)
        if not account:
            raise forms.ValidationError('No se ha detectado cuenta en uso')
        return account


class CategoryFormComponent(HTMXFormView, component.Component):
    form_class = CategoryForm
    success_url = '.'
    action_url = 'category-form'


class CategoryUpdateFormComponent(HTMXObjectFormView, component.Component):
    queryset = Category.objects.none()
    form_class = CategoryForm
    success_url = '.'
    action_url = 'category-update-form'

    def get_queryset(self):
        current_account = get_current_account(self.request)
        return Category.objects.filter(account=current_account)


class CategoryDeleteFormComponent(HTMXDeleteFormView, component.Component):
    success_url = '.'
    action_url = 'category-delete-form'

    def get_queryset(self):
        current_account = get_current_account(self.request)
        return Category.objects.filter(account=current_account)


