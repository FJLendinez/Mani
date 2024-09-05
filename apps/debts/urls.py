from django.urls import path

from apps.debts import views

urlpatterns = [
    path('', views.debts_view, name='debt_list'),
]
