from django.urls import path

from components.categories.categories_form import CategoryDeleteFormComponent, CategoryUpdateFormComponent, \
    CategoryFormComponent
from components.debts.debts_form import DebtFormComponent, DebtUpdateFormComponent, DebtDeleteFormComponent
from components.goals.goal_form import GoalFormComponent, GoalUpdateFormComponent, GoalDeleteFormComponent
from components.header.set_month import DateRangeSetterComponent
from components.transactions.deposit import DepositComponent
from components.transactions.transaction_form import TransactionFormComponent, TransactionUpdateFormComponent, \
    TransactionDeleteFormComponent
from components.transactions.transfer import TransferComponent

urlpatterns = [
    path('transaction-form/', TransactionFormComponent.as_view(), name='transaction-form'),
    path('transaction-form/<str:pk>/', TransactionUpdateFormComponent.as_view(), name='transaction-update-form'),
    path('transaction-form/<str:pk>/delete/', TransactionDeleteFormComponent.as_view(), name='transaction-delete-form'),
    path('goal-form/', GoalFormComponent.as_view(), name='goal-form'),
    path('goal-form/<str:pk>/', GoalUpdateFormComponent.as_view(), name='goal-update-form'),
    path('goal-form/<str:pk>/delete/', GoalDeleteFormComponent.as_view(), name='goal-delete-form'),
    path('category-form/', CategoryFormComponent.as_view(), name='category-form'),
    path('category-form/<str:pk>/', CategoryUpdateFormComponent.as_view(), name='category-update-form'),
    path('category-form/<str:pk>/delete/', CategoryDeleteFormComponent.as_view(), name='category-delete-form'),
    path('debt-form/', DebtFormComponent.as_view(), name='debt-form'),
    path('debt-form/<str:pk>/', DebtUpdateFormComponent.as_view(), name='debt-update-form'),
    path('debt-form/<str:pk>/delete/', DebtDeleteFormComponent.as_view(), name='debt-delete-form'),
    path('transfer/', TransferComponent.as_view(), name='transfer'),
    path('deposit/', DepositComponent.as_view(), name='deposit'),
    path('set-date/', DateRangeSetterComponent.as_view(), name='set-month'),
]
