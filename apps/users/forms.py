from django import forms
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.forms import ModelForm, Form

from apps.users.models import User


class UserUpdateForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class UserChangePasswordForm(Form):
    password = forms.CharField(widget=forms.PasswordInput)
    repeat_password = forms.CharField(widget=forms.PasswordInput)

    def clean_password(self):
        validate_password(self.data['password'])
        return self.data['password']

    def clean_repeat_password(self):
        if self.data['password'] != self.data['repeat_password']:
            raise ValidationError('La contraseña no coincide')

    def clean(self):
        if self.data['password'] != self.data['repeat_password']:
            raise ValidationError('Deben coincidir las contraseñas')
        return self.cleaned_data
