from locale import currency
from django.db import models
from django.contrib.auth import get_user_model

User= get_user_model()
# Create your models here.

class Calculation(models.Model):
    user= models.ForeignKey(User, blank=True, on_delete= models.CASCADE, related_name="calculation")
    description= models.CharField(max_length=255, blank=True, null=True)
    duty= models.CharField(max_length=255, blank=True, null=True)
    cost= models.CharField(max_length=255, blank=True, null=True)

class Rate(models.Model):
    currency_name= models.CharField(max_length=255, blank=True, null=True)
    currency_code= models.CharField(max_length=255, blank=True, null=True)
    exchange_rate= models.FloatField(blank=True, null=True)


class Tariff(models.Model):
    hs_description= models.CharField(max_length=255, blank=True, null=True)
    hscode= models.CharField(max_length=255, blank=True, null=True)
    su= models.CharField(max_length=255, blank=True, null=True)
    id_tariff= models.CharField(max_length=255, blank=True, null=True)
    vat= models.CharField(max_length=255, blank=True, null=True)

