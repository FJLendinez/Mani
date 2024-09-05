"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from apps.core.views import index, send_test_email, store_in_cache

urlpatterns = [
    path("", index),
    path("", include('apps.users.urls')),
    path('components/', include('components.urls')),
    path("send-email/", send_test_email),
    path("store-cache/", store_in_cache),
    path("admin/", admin.site.urls),
    path("transactions/", include('apps.transactions.urls')),
    path("accounts/", include('apps.accounts.urls')),
    path("goals/", include('apps.goals.urls')),
    path("debts/", include('apps.debts.urls')),
    path('webpush/', include('webpush.urls'))

]
