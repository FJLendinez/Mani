from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group as DjangoGroup
from django.utils.translation import gettext_lazy as _

from apps.users.models import User


admin.site.unregister(DjangoGroup)

class Group(DjangoGroup):
    class Meta:
        proxy = True
        verbose_name = _("group")
        verbose_name_plural = _("groups")
        

admin.site.register(User, UserAdmin)
admin.site.register(Group)
