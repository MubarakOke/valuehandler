from django.contrib import admin
from operations import  models
# Register your models here.

admin.site.register(models.Calculation)
admin.site.register(models.Rate)
admin.site.register(models.Tariff)