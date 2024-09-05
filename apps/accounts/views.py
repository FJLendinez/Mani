from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from apps.accounts.service.accounts import set_current_account
from apps.core.utils import client_redirect


@login_required()
def set_current_account_view(request):
    set_current_account(request, request.GET.get('accountid'))
    return client_redirect('.')
