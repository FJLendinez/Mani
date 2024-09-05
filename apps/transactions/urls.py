from django.urls import path

from apps.transactions import views

urlpatterns = [
    path('', views.transactions, name='transaction_list'),
    path('categories/', views.categories, name='category_list'),
]