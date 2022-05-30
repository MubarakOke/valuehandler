from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from accounts import serializers


# Create your views here.
class RegistrationView(CreateAPIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    permission_classes= [] 
    authentication_classes=[]
    serializer_class= serializers.UserSerializer
