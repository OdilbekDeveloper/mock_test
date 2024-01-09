from django.db import models
from apps.main.models import User

class ClickOrder(models.Model):
    is_paid = models.BooleanField(default=False)
    amount = models.DecimalField(decimal_places=2, max_digits=12)
    user = models.ForeignKey(User, on_delete=models.PROTECT)