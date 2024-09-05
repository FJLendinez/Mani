from django.contrib.auth.views import logout_then_login
from django.urls import path

from .views import login_view, user_settings, change_password

app_name = 'users'

urlpatterns = [
    path("login/", login_view, name='login'),
    path("logout/", logout_then_login, name='logout'),
    path("user/settings/", user_settings, name='user_settings'),
    path("user/change_password/", change_password, name='change_password'),
]
