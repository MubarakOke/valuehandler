
from django.shortcuts import render
from rest_framework.generics import GenericAPIView,UpdateAPIView
from rest_framework.mixins import ListModelMixin, UpdateModelMixin




from .models import Rate, Tariff, Calculation 
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
import pandas as pd
from rest_framework.response import Response
from operations import  serializers

from django.contrib.auth import get_user_model
from .utils import convertnan
from rest_framework import permissions

User=get_user_model()

# Create your views here.

class CalculationPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        staff=request.user.is_staff
        if request.method in permissions.SAFE_METHODS:
            if staff:
                return True
            
            return False
        else:
            if request.user.is_authenticated():
                return True
            return False


class RateView(ListModelMixin, GenericAPIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    permission_classes= [] 
    serializer_class= serializers.RateSerializer
    authentication_classes=[]
    queryset= Rate.objects.all()

    def post(self, request, *args, **kwargs):
        file_uploaded= request.FILES.get('file_upload')
        try:
            file= pd.read_excel(file_uploaded).to_dict(orient='records')
        except:
            return Response({"error": "please upload excel"}, status=400)
        try:
            rate_list= [Rate(currency_name=value['Name'], currency_code=value['Code'], exchange_rate=value['Exchange rate']) for value in file]
        except:
            return Response({"error": "ensure currency_name, currency_code and exchange_rate are in excel file"}, status=400)
        Rate.objects.all().delete()
        Rate.objects.bulk_create(rate_list)
        return Response({"detail": "uploaded successfully"}, status=200)
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class RateDetailView(UpdateAPIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    permission_classes= [] 
    serializer_class= serializers.RateSerializer
    authentication_classes=[]
    queryset= Rate.objects.all()
    lookup_field= 'id'


class TariffView(ListModelMixin, GenericAPIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    permission_classes= [] 
    authentication_classes=[]
    serializer_class= serializers.TariffSerializer
    queryset= Tariff.objects.all()

    def post(self, request, *args, **kwargs):
        file_uploaded= request.FILES.get('file_upload')
        try:
            file= pd.read_excel(file_uploaded).to_dict(orient='records')
        except:
            return Response({"error": "please upload excel"}, status=400)  
        rate_list_converted= convertnan(file)
        try:
            rate_list= [Tariff(hs_description=value['Description'], hscode=value['CET Code'], su=value['SU'], id_tariff=value['ID'], vat=value['VAT'], levy=value['LVY'], e_duty=value['EXC'])  for value in rate_list_converted]
        except:
            return Response({"error": "ensure HSCODE DESCRIPTION, HSCODE, SU, ID an VAT are in excel file"}, status=400)
        Tariff.objects.all().delete()
        Tariff.objects.bulk_create(rate_list)
        return Response({"detail": "uploaded successfully"}, status=200)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

class TariffDetailView(UpdateAPIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    permission_classes= [] 
    serializer_class= serializers.TariffSerializer
    authentication_classes=[]
    queryset= Tariff.objects.all()
    lookup_field= 'id'



class CalculationView(ListModelMixin, GenericAPIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    permission_classes= [CalculationPermission]
    serializer_class= serializers.CalculationSerializer
    queryset= Calculation.objects.all()

    def post(self, request, *args, **kwargs):
        hscode= request.data.get('hscode')
        hscode_description= request.data.get('hscode_description')
        item_description= request.data.get('item_description')
        currency= request.data.get('currency')
        insurance= request.data.get('insurance', None)
        insurance_percentage= request.data.get('insurance_percentage', None)
        fob= request.data.get('fob')
        freight= request.data.get('freight')  

        if (not hscode or not hscode_description or not item_description or not currency or not fob or not freight)  or (not insurance and not insurance_percentage):
            return Response({"error": "please pass all the parameters"}, status=400)
        try:
            rate_obj= Rate.objects.get(currency_code=currency)
            tariff_obj= Tariff.objects.get(hscode=hscode)
        except:
            return Response({"error": "this currency does not exist"}, status=400)

        cf= float(fob) + float(freight)
        if insurance:
            i= insurance
        else:   
            i= insurance_percentage/100 * cf
        cif= cf + i
        cif= cif
        id=  float(tariff_obj.id_tariff)/100 * float(cif)
        sc= 0.07 * float(id)
        ciss= 0.01 * float(fob)
        etls= 0.005 * float(cif)
        vat= float(tariff_obj.vat)/100 * float((cif + id + sc+ ciss + etls))
        levy= float(tariff_obj.levy)/100 * float(cif)
        exercise_duty= float(tariff_obj.e_duty)/100 * float(cif)
        custom_duty= float((id + sc + ciss + etls + vat)) + float(levy) +float(exercise_duty)
        custom_duty_naira= float(custom_duty) * float(rate_obj.exchange_rate)
        total_cost= float(fob) + float(custom_duty)
        total_cost_naira= float(total_cost) * float(rate_obj.exchange_rate)

        calculation_obj= Calculation.objects.create(user=request.user, description=item_description, duty=custom_duty_naira, cost=total_cost_naira)
        calculation_obj.save()
        return Response({"detail": {f"result": custom_duty,
                                    f"total": total_cost,
                                    "result_NGN": custom_duty_naira,
                                    "total_NGN": total_cost_naira
                                    }}, status=200)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
