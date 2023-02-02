from django.db import models
from django.utils import timezone

# Create your models here.


class ClearHistoryModel(models.Model):
    user = models.CharField(max_length=20)
    date = models.DateField(verbose_name='日付', default=timezone.now)
