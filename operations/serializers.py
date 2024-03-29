from rest_framework import serializers
from operations.models import (Calculation, Rate, Tariff) 
from accounts.serializers import UserSerializer, UserRegisterSerializer 

class CalculationSerializer(serializers.ModelSerializer):
    user= UserRegisterSerializer(read_only=True)
    class Meta:
        model= Calculation
        fields= [
            'user',
            'description',
            'duty',
            'cost',
            'timestamp'
        ]
    


class RateSerializer(serializers.ModelSerializer):
    class Meta:
        model= Rate
        fields= [
                    'id',
                    'currency_name',
                    'currency_code',
                    'exchange_rate',
                    'date_uploaded'
                ] 

class TariffSerializer(serializers.ModelSerializer):
    class Meta:
        model= Tariff
        fields= [
                    'hs_description',
                    'hscode',
                    'su',
                    'id_tariff',
                    'levy',
                    'vat',
                    'e_duty',
                    'date_uploaded'
                ] 
        extra_kwargs= {'hscode':{'required':False}} 