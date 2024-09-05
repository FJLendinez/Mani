from django.db import models

from apps.users.models import User


# Create your models here.
class Account(models.Model):
    name = models.CharField(max_length=120)
    users = models.ManyToManyField(User, related_name='accounts')

    def __str__(self):
        return f"[{self.id}] {self.name} - {' '.join(self.users.all().values_list('username', flat=True))}"