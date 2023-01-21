from locale import currency
from uuid import uuid4
from django.db import models
from django.contrib.auth import get_user_model


User= get_user_model()
# Create your models here.

class Calculation(models.Model):
    user= models.ForeignKey(User, blank=True, on_delete= models.CASCADE, related_name="calculation")
    description= models.CharField(max_length=255, blank=True, null=True)
    duty= models.CharField(max_length=255, blank=True, null=True)
    cost= models.CharField(max_length=255, blank=True, null=True)
    timestamp= models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['-id']

class Rate(models.Model):
    id= models.UUIDField(primary_key=True, default=uuid4, editable=False)
    currency_name= models.CharField(max_length=255, blank=True, null=True)
    currency_code= models.CharField(max_length=255, blank=True, null=True)
    exchange_rate= models.FloatField(blank=True, null=True)
    date_uploaded= models.DateTimeField(auto_now=True)

class Tariff(models.Model):
    hs_description= models.CharField(max_length=255, blank=True, null=True)
    hscode= models.CharField(max_length=255, blank=False, null=False, primary_key=True)
    su= models.CharField(max_length=255, blank=True, null=True)
    id_tariff= models.CharField(max_length=255, blank=True, null=True)
    vat= models.CharField(max_length=255, blank=True, null=True)
    levy= models.CharField(max_length=255, blank=True, null=True)
    e_duty= models.CharField(max_length=255, blank=True, null=True)
    date_uploaded= models.DateTimeField(auto_now=True)

