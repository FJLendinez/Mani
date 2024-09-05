from django_components import component

from apps.accounts.service.accounts import get_accounts, get_current_account, get_total_in_account


@component.register("header_menu")
class HeaderMenuComponent(component.Component):
    template_name = 'header/header__menu.html'

    def get_context_data(self, request, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_accounts'] = get_accounts(request)
        context['current_account'] = get_current_account(request)
        context['total_in_account'] = get_total_in_account(request)
        return context