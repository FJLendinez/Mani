from django.urls import path

from .views import set_current_account_view

app_name = 'accounts'

urlpatterns = [
    path("set-current/", set_current_account_view, name='set_current_account_view')
]
