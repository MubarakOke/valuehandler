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
        ]
    


class RateSerializer(serializers.ModelSerializer):
    class Meta:
        model= Rate
        fields= [
                    'id',
                    'currency_name',
                    'currency_code',
                    'exchange_rate'
                ] 


class TariffSerializer(serializers.Serializer):
    file_upload= serializers.FileField()
    class Meta:
        fields= ['file_upload']