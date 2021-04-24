from django.db import models
from django.contrib.auth.models import AbstractUser


class TheSloiksUser(AbstractUser):
    pass


class Jar(models.Model):
    balance = models.DecimalField(max_digits=20, decimal_places=2)
    currency = models.CharField(max_length=3, default='PLN')


class Transaction(models.Model):
    date_created = models.DateTimeField()
    value = models.DecimalField(max_digits=20, decimal_places=2)
    title = models.CharField(max_length=250)
    type = models.CharField(max_length=8, default='')
    target_jar = models.ForeignKey(Jar, on_delete=models.CASCADE, related_name='target_jar', blank=True, null=True)
    source_jar = models.ForeignKey(Jar, on_delete=models.CASCADE, related_name='source_jar', blank=True, null=True)
    currency = models.CharField(max_length=3, default='PLN')
