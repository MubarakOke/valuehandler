from django.shortcuts import render
from rest_framework.generics import GenericAPIView, CreateAPIView, DestroyAPIView, UpdateAPIView
from rest_framework.mixins import ListModelMixin, UpdateModelMixin
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Rate, Tariff, Calculation 
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
import pandas as pd
from rest_framework.response import Response
from operations import  serializers
from accounts.serializers import UserRegisterSerializer
from django.contrib.auth import get_user_model
User=get_user_model()

# Create your views here.

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
            rate_list= [Rate(currency_name=value['currency name'], currency_code=value['currency code'], exchange_rate=value['exchange rate']) for value in file]
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


class TariffView(GenericAPIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    permission_classes= [] 
    authentication_classes=[]
    queryset= Tariff.objects.all()

    def post(self, request, *args, **kwargs):
        file_uploaded= request.FILES.get('file_upload')
        try:
            file= pd.read_excel(file_uploaded).to_dict(orient='record')
        except:
            return Response({"error": "please upload excel"}, status=400)
        
        try:
            rate_list= [Tariff(hs_description=value['HSCODE DESCRIPTION'], hscode=value['HSCODE'], su=value['SU'], id_tariff=value['ID'], vat=value['VAT']) for value in file]
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
    permission_classes= [IsAuthenticated]
    serializer_class= serializers.CalculationSerializer
    queryset= Calculation.objects.all()

    def post(self, request, *args, **kwargs):
        hscode= request.data.get('hscode')
        hscode_description= request.data.get('hscode_description')
        item_description= request.data.get('item_description')
        currency= request.data.get('currency')
        insurance= request.data.get('insurance')
        fob= request.data.get('fob')
        freight= request.data.get('freight')  
        if not hscode or not hscode_description or not item_description or not currency or not insurance or not fob or not freight:
            return Response({"error": "please pass all the parameters"}, status=400)
        try:
            rate_obj= Rate.objects.get(currency_name=currency)
        except:
            return Response({"error": "this currency does not exist"}, status=400)

        cf= float(fob) + float(freight)
        i= insurance * cf
        cif= cf + i
        cif_to_naira= cif * rate_obj.exchange_rate
        id= float(hscode) * cif_to_naira
        sc= 0.07 * id
        ciss= 0.01 * fob
        etls= 0.005 * cif_to_naira
        vat= 0.075 * (cif_to_naira + id + sc+ ciss + etls)
        levy= hscode * cif_to_naira
        exercise_duty= hscode * cif_to_naira
        custom_duty= (id + sc + ciss + etls + vat) + levy + exercise_duty
        total_cost= fob + custom_duty
        calculation_obj= Calculation.objects.create(user=request.user, description=item_description, duty=custom_duty, cost=total_cost)
        calculation_obj.save()
        return Response({"detail": {"result": custom_duty,
                                    "total": total_cost}}, status=200)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
