from rest_framework import serializers
from operations.models import (Calculation, Rate, Tariff) 
from accounts.serializers import UserSerializer

class CalculationSerializer(serializers.ModelSerializer):
    user= UserSerializer(read_only=True)
    class Meta:
        model= Calculation
        fields= [
            'user',
            'description',
            'duty',
            'cost',
        ]
    
    def create(self, validated_data):
        calculation_obj= Calculation.objects.create(decription=validated_data.get('decription'), duty=validated_data.get('duty'), cost=validated_data.get('cost'))
        calculation_obj.save()
        return calculation_obj


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