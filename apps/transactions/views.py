from datetime import date

from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render
from django.urls import reverse
from django.utils.safestring import mark_safe

from apps.transactions.models import Transaction
from apps.transactions.service.categories import get_categories, add_total_expenses
from apps.transactions.service.transactions import get_current_transactions, get_current_account_transactions


@login_required()
def transactions(request):
    acc_transactions = get_current_account_transactions(request)
    transactions = get_current_transactions(request).order_by('-date', '-id')
    today = date.today()
    current_transaction_history = acc_transactions.filter(date__lte=today)

    def to_value(qs):
        return qs.aggregate(Sum('amount')).get('amount__sum') or 0

    total_income = to_value(current_transaction_history.filter(type=Transaction.TransactionType.INCOME))
    total_expenses = to_value(
        current_transaction_history.filter(type=Transaction.TransactionType.EXPENSE, goal__isnull=True))
    total_deposit = to_value(
        current_transaction_history.filter(type=Transaction.TransactionType.EXPENSE, goal__isnull=False))
    return render(request, 'pages/transactions/transactions_list.html', {'transactions': transactions,
                                                                         'headings': ['Concepto', 'Cantidad', 'Fecha',
                                                                                      'Categoría', 'Objetivo', 'Deuda',
                                                                                      'Acciones'],
                                                                         'fields': [lambda x: x.description,
                                                                                    lambda
                                                                                        x: f"{'-' if x.type == Transaction.TransactionType.EXPENSE else ''}{x.amount} €",
                                                                                    lambda x: x.date,
                                                                                    lambda
                                                                                        x: x.category and x.category.name or '',
                                                                                    lambda
                                                                                        x: x.goal and x.goal.name or '',
                                                                                    lambda
                                                                                        x: x.debt and x.debt.name or '',
                                                                                    lambda x: mark_safe(
                                                                                        f"""<button class="btn btn-sm btn-outline btn-primary" hx-get="{reverse('transaction-update-form', args=[x.id])}" hx-target="#modal-content">Editar
                                                                                           </button>
                                                                                           <button class="btn btn-sm btn-outline btn-secondary" hx-get="{reverse('transaction-delete-form', args=[x.id])}" hx-target="#modal-content">Eliminar
                                                                                           </button>
                                                                                                                                       """)
                                                                                    ],
                                                                         'total_income': total_income,
                                                                         'total_expenses': total_expenses,
                                                                         'total_deposit': total_deposit,
                                                                         'total': total_income - total_expenses - total_deposit,
                                                                         'total_real': total_income - total_expenses,
                                                                         })


@login_required()
def categories(request):
    cats = get_categories(request)
    cats = add_total_expenses(request, cats)
    total_estimated = cats.aggregate(Sum('estimated')).get('estimated__sum') or 0
    total_expenses = cats.aggregate(Sum('total_expenses')).get('total_expenses__sum') or 0
    prop = (total_expenses / total_estimated if total_estimated else 0) * 100
    return render(request, 'pages/category/list.html', {'categories': cats,
                                                        'headings': ['Categoría',
                                                                     'Estimación de gasto',
                                                                     'Gastado',
                                                                     'Acciones'],
                                                        'fields': [lambda x: x.name,
                                                                   lambda x: f"{x.estimated} €",
                                                                   lambda x: f"{x.total_expenses or 0:.2f} €",
                                                                   lambda x: mark_safe(
                                                                       f"""<button class="btn btn-sm btn-outline btn-primary" hx-get="{reverse('category-update-form', args=[x.id])}" hx-target="#modal-content">Editar
                                                                                       </button>
                                                                                       <button class="btn btn-sm btn-outline btn-secondary" hx-get="{reverse('category-delete-form', args=[x.id])}" hx-target="#modal-content">Eliminar
                                                                                       </button>
                                                                                                                                   """)
                                                                   ],
                                                        'total_estimated': total_estimated,
                                                        'prop': prop,
                                                        })
