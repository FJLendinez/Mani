from django.contrib import admin

from apps.transactions.models import Transaction, Category

# Register your models here.
admin.site.register(Category)
admin.site.register(Transaction)
