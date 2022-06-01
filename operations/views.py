from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from .models import Rate, Tariff, Calculation 
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
import pandas as pd
from rest_framework.response import Response
from operations import  serializers
# Create your views here.

class RateUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    permission_classes= [] 
    authentication_classes=[]

    def post(self, request, *args, **kwargs):
        file_uploaded= request.FILES.get('file_upload')
        try:
            file= pd.read_excel(file_uploaded).to_dict(orient='record')
        except:
            return Response({"error": "please upload excel"}, status=400)
        try:
            rate_list= [Rate(currency_name=value['currency name'], currency_code=value['currency code'], exchange_rate=value['exchange rate']) for value in file]
        except:
            return Response({"error": "ensure currency_name, currency_code and exchange_rate are in excel file"}, status=400)
        Rate.objects.all().delete()
        Rate.objects.bulk_create(rate_list)
        return Response({"detail": "uploaded successfully"}, status=200)

class RateListView(ListAPIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    permission_classes= [] 
    authentication_classes=[]
    serializer_class= serializers.RateSerializer
    queryset= Rate.objects.all()

class TariffUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    permission_classes= [] 
    authentication_classes=[]

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
        # Tariff.objects.all().delete()
        Tariff.objects.bulk_create(rate_list)
        return Response({"detail": "uploaded successfully"}, status=200)