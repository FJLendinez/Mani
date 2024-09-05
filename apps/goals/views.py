from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render
from django.urls import reverse
from django.utils.safestring import mark_safe

from apps.goals.service.goals import get_goals, add_total_expenses, deposit_on_period


@login_required()
def goals(request):
    goals = get_goals(request)
    saved_on_period = deposit_on_period(request, goals)
    goals = add_total_expenses(goals)
    total_saved = goals.aggregate(Sum('transactions__amount')).get('transactions__amount__sum') or 0
    total_required = goals.aggregate(Sum('amount')).get('amount__sum') or 0

    return render(request, 'pages/goals/list.html', {'goals': goals,
                                                     'headings': ['Objetivo',
                                                                  'Fecha límite',
                                                                  'Cantidad a ahorrar',
                                                                  'Cantidad ahorrada',
                                                                  'Acciones', ],
                                                     'fields': [lambda x: x.name,
                                                                lambda x: x.date,
                                                                lambda x: f"{x.amount} €",
                                                                lambda x: f"{x.total_expenses or 0} €",
                                                                lambda x: mark_safe(f"""
                                                                 <button class="btn btn-sm btn-outline btn-primary" hx-get="{reverse('goal-update-form', args=[x.id])}" hx-target="#modal-content">Editar
                    </button>
                    <button class="btn btn-sm btn-outline btn-secondary" hx-get="{reverse('goal-delete-form', args=[x.id])}" hx-target="#modal-content">Eliminar
                    </button>
                                                                """)],
                                                     'saved_on_period': saved_on_period,
                                                     'total_saved': total_saved,
                                                     'total_required': total_required,
                                                     })
