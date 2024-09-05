from datetime import date, timedelta

from django_components import component

from apps.core.utils import client_redirect


def get_previous_period(date_from, period='month'):
    start_date = get_start_of_period(date_from, period) - timedelta(days=1)
    return get_start_of_period(start_date)
    # if period == 'year':
    #     prev_date_from = date_from.replace(year=date_from.year - 1, month=1, day=1)
    # elif period == 'week':
    #     prev_date_from = date_from - timedelta(days=7)
    # else:
    #     try:
    #         prev_date_from = date_from.replace(month=date_from.month - 1)
    #     except:
    #         prev_date_from = date_from.replace(month=12, year=date_from.year - 1)
    # return prev_date_from
    #


def get_next_period(date_from, period='month'):
    if period == 'year':
        next_date_from = date_from.replace(year=date_from.year + 1, month=1, day=1)
    elif period == 'week':
        next_date_from = date_from + timedelta(days=7)
    elif period == 'quarter':
        quarter = (date_from.month - 1) // 3 + 1
        return date(date_from.year + 3 * quarter // 12, 3 * quarter % 12 + 1, date_from.day)
    else:
        try:
            next_date_from = date_from.replace(month=date_from.month + 1)
        except:
            next_date_from = date_from.replace(month=1, year=date_from.year + 1)
    return next_date_from


def get_start_of_period(date_from, period='month'):
    if period == 'year':
        return date_from.replace(year=date_from.year, month=1, day=1)
    if period == 'month':
        return date_from.replace(day=1)
    if period == 'quarter':
        return date(date_from.year, 3 * ((date_from.month - 1) // 3) + 1, 1)
    return date_from


def get_end_of_period(date_from, period='month'):
    next_date_from = get_next_period(date_from, period)
    return next_date_from - timedelta(days=1)


def set_current_date(request, date_from, period='month'):
    request.session['period'] = period or 'month'
    if not date_from:
        request.session['date_from'] = None
        return
    request.session['date_from'] = date_from.isoformat()


def get_current_date(request):
    p = request.session.get('period') or 'month'
    d_from = request.session.get('date_from') or date.today().replace(day=1).isoformat()
    d_from = get_start_of_period(date.fromisoformat(d_from), p)
    d_to = get_end_of_period(d_from, p)
    return d_from, d_to


@component.register('date_range_setter')
class DateRangeSetterComponent(component.Component):
    template = """
    <div class="flex">
<div class="join gap-0">
  <a href="/components/set-date/?previous=true type="button" class="btn btn-xs	 join-item"><</a>
  <a href="/components/set-date/?now=true" type="button" class="btn btn-xs	join-item hidden lg:flex">{% if range_from and range_to %}{{ range_from }} - {{ range_to }}{% endif %}</a>
  <a href="/components/set-date/?now=true" type="button" class="btn btn-xs	join-item flex lg:hidden">{% if range_from and range_to %}{{ range_from.isoformat }} - {{ range_to.isoformat }}{% endif %}</a>
  <a href="/components/set-date/?period={{ next_period }}" type="button" class="btn btn-xs	 join-item">{{ period }}</a>
  <a href="/components/set-date/?next=true"type="button" class="btn btn-xs	 join-item">></a>
</div>
</div>
"""

    def get_context_data(self, request, **kwargs):
        d_from, d_to = get_current_date(request)
        periods = {'year': 'Año', 'month': 'Mes', 'quarter': 'Trimestre'}
        periods_k = list(periods.keys())
        period = request.session.get('period') or 'month'
        next_period_type = periods_k[(periods_k.index(period) + 1) % len(periods)]

        context = {'range_from': d_from, 'range_to': d_to, 'period': periods.get(period),
                   'next_period': next_period_type}
        return context

    def get(self, request, *args, **kwargs):
        d_from = date.fromisoformat(request.session.get('date_from') or date.today().replace(day=1).isoformat())
        p = request.GET.get('period') or request.session.get('period')
        if request.GET.get('previous', False):
            d_from = get_previous_period(d_from, p)
        elif request.GET.get('next', False):
            d_from = get_next_period(d_from, p)
        elif request.GET.get('now', False):
            d_from = date.today().replace(day=1)

        set_current_date(request, d_from, p)
        return client_redirect('.')
