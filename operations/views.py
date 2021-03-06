
from django.shortcuts import render
from rest_framework.generics import GenericAPIView,UpdateAPIView
from rest_framework.mixins import ListModelMixin, UpdateModelMixin
from rest_framework.views import APIView



from .models import Rate, Tariff, Calculation 
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
import pandas as pd
from rest_framework.response import Response
from operations import  serializers

from django.contrib.auth import get_user_model
from .utils import convertnan
# from rest_framework import permissions

User=get_user_model()

# Create your views here.

# class CalculationPermission(permissions.BasePermission):
#     def has_permission(self, request, view):
#         staff=request.user.is_staff
#         if request.method in permissions.SAFE_METHODS:
#             if staff:
#                 return True
            
#             return False
#         else:
#             if request.user.is_authenticated():
#                 return True
#             return False


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
        return Response({"detail": "uploaded successfully"}, status=201)
    
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
        return Response({"detail": "uploaded successfully"}, status=201)

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
    permission_classes= []
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
        except:
            return Response({"error": "this currency does not exist"}, status=400)
        
        try:
            tariff_obj= Tariff.objects.get(hscode=hscode)
        except:
            return Response({"error": "this tariff does not exist"}, status=400)

        cf= float(fob) + float(freight)
        cf_NGN= cf * float(rate_obj.exchange_rate)
        if insurance:
            i= insurance
        else:   
            i= insurance_percentage/100 * cf
        cif= cf + i
        cif_NGN=cif * float(rate_obj.exchange_rate)
        id=  float(tariff_obj.id_tariff)/100 * float(cif)
        id_NGN= id * float(rate_obj.exchange_rate)
        sc= 0.07 * float(id)
        sc_NGN= sc * float(rate_obj.exchange_rate)
        ciss= 0.01 * float(fob)
        ciss_NGN= ciss * float(rate_obj.exchange_rate)
        etls= 0.005 * float(cif)
        etls_NGN= etls * float(rate_obj.exchange_rate)
        vat= float(tariff_obj.vat)/100 * float((cif + id + sc+ ciss + etls))
        vat_NGN= vat * float(rate_obj.exchange_rate)
        levy= float(tariff_obj.levy)/100 * float(cif)
        levy_NGN= levy * float(rate_obj.exchange_rate)
        exercise_duty= float(tariff_obj.e_duty)/100 * float(cif)
        exercise_duty_NGN= exercise_duty * float(rate_obj.exchange_rate)
        custom_duty= float((id + sc + ciss + etls + vat)) + float(levy) +float(exercise_duty)
        custom_duty_NGN= float(custom_duty) * float(rate_obj.exchange_rate)

        total_cost= float(fob) + float(custom_duty)
        total_cost_naira= float(total_cost) * float(rate_obj.exchange_rate)

        calculation_obj= Calculation.objects.create(user=request.user, description=item_description, duty=custom_duty_NGN, cost=total_cost_naira)
        calculation_obj.save()
        return Response({"detail": {"result": custom_duty,
                                    "result_NGN": custom_duty_NGN,
                                    "total": total_cost,    
                                    "total_NGN": total_cost_naira,
                                    "cf":cf,
                                    "cf_NGN":cf_NGN,
                                    "cif":cif,
                                    "cif_NGN":cif_NGN,
                                    "id":id,
                                    "id_NGN":id_NGN,
                                    "sc":sc,
                                    "sc_NGN":sc_NGN,
                                    "ciss":ciss,
                                    "ciss_NGN":ciss_NGN,
                                    "etls":etls,
                                    "etls_NGN":etls_NGN,
                                    "vat":vat,
                                    "vat_NGN":vat_NGN,
                                    "levy":levy,
                                    "levy_NGN":levy_NGN,
                                    "exercise_duty":exercise_duty,
                                    "exercise_duty_NGN":exercise_duty_NGN
                                    }}, status=200)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

class RateTariffView(APIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    permission_classes= []

    def get(self, request, *args, **kwargs):
        rate= Rate.objects.all()
        rate_serialized= serializers.RateSerializer(rate, many=True).data
        tariff= Tariff.objects.all()
        tariff_serialized=  serializers.TariffSerializer(tariff, many=True).data

        return Response({"rate": rate_serialized,
                         "tariff": tariff_serialized}, status=200)