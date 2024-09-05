from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse
from django.utils.safestring import mark_safe

from apps.accounts.service.accounts import get_current_account
from apps.debts.models import Debt


# Create your views here.
@login_required()
def debts_view(request):
    debts = Debt.objects.filter(account=get_current_account(request), archived=False)
    debts = Debt.aggregate_amount(debts)
    lend_debts = debts.filter(type=Debt.DebtType.LEND)
    loan_debts = debts.filter(type=Debt.DebtType.LOAN)
    return render(request, 'pages/debt/list.html', {'lend_debts': lend_debts,
                                                    'lend_headings': ['Deuda',
                                                                      'Dinero prestado',
                                                                      'Recuperado',
                                                                      'Acciones'],
                                                    'lend_fields': [lambda x: x.name,
                                                                    lambda
                                                                        x: f"{x.transactions_expense or 0} €",
                                                                    lambda
                                                                        x: f"{x.transactions_income or 0} €",
                                                                    lambda x: mark_safe(f"""
                                                                       <button class="btn btn-sm btn-outline btn-primary" hx-get="{reverse('debt-update-form', args=[x.id])}" hx-target="#modal-content">Editar
                                                                       </button>
                                                                       <button class="btn btn-sm btn-outline btn-secondary" hx-get="{reverse('debt-delete-form', args=[x.id])}" hx-target="#modal-content">Archivar
                                                                       </button>
                                                                        """)
                                                                    ],
                                                    'loan_debts': loan_debts,
                                                    'loan_headings': ['Deuda',
                                                                      'Dinero pedido',
                                                                      'Amortizado',
                                                                      'Acciones'],
                                                    'loan_fields': [lambda x: x.name,
                                                                    lambda
                                                                        x: f"{x.transactions_income or 0} €",
                                                                    lambda
                                                                        x: f"{x.transactions_expense or 0} €",
                                                                    lambda x: mark_safe(f"""
                                                                           <button class="btn btn-sm btn-outline btn-primary" hx-get="{reverse('debt-update-form', args=[x.id])}" hx-target="#modal-content">Editar
                                                                           </button>
                                                                           <button class="btn btn-sm btn-outline btn-secondary" hx-get="{reverse('debt-delete-form', args=[x.id])}" hx-target="#modal-content">Eliminar
                                                                           </button>
                                                                            """)
                                                                    ]
                                                    })
