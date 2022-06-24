from django.shortcuts import render
from rest_framework.generics import CreateAPIView,ListAPIView,UpdateAPIView
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from accounts import serializers
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.serializers import UserSerializer, UserRegisterSerializer

User = get_user_model()

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

# Create your views here.
class RegistrationView(CreateAPIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    permission_classes= [] 
    authentication_classes=[]
    serializer_class= serializers.UserSerializer

class AuthenticateView(APIView):
    permission_classes= []
    authentication_classes= []

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return Response({"detail":"You are already authenticated"}, status= 400)
        email= request.data.get('email', None)
        password= request.data.get('password', None)

        if not email and not password:
            return Response({"error": "Please enter your email and password"}, status=400)

        obj= User.objects.filter(Q(email__iexact= email))
            
        if obj and obj.count()==1:
            user_obj= obj.first() 
            if user_obj.check_password(password):
                token= get_tokens_for_user(user_obj)
                return Response({
                                "token": token["access"],
                                "user": UserRegisterSerializer(user_obj).data,                                           
                                }, status=200)
        return Response({"error": "invalid login details"}, status=400)

# class AuthenticateAdminView(APIView):
#     permission_classes= []
#     authentication_classes= []

#     def post(self, request, *args, **kwargs):
#         if request.user.is_authenticated:
#             return Response({"detail":"You are already authenticated"}, status= 400)
#         email= request.data.get('email', None)
#         password= request.data.get('password', None)

#         if not email and not password:
#             return Response({"error": "Please enter your email and password"}, status=400)

#         obj= User.objects.filter(Q(email__iexact= email))
            
#         if obj and obj.count()==1:
#             user_obj= obj.first() 
#             if user_obj.check_password(password) and user_obj.user_type.capitalize() == 'Admin':
#                 token= get_tokens_for_user(user_obj)
#                 return Response({
#                                 "token": token["access"],
#                                 "user": UserRegisterSerializer(user_obj).data,                                           
#                                 }, status=200)
#         return Response({"error": "invalid login details"}, status=400)


class UserListView(ListAPIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    permission_classes = [permissions.IsAdminUser]
    serializer_class= UserRegisterSerializer
    queryset= User.objects.all()

class EditUserRoleView(UpdateAPIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    serializer_class= UserRegisterSerializer   
    lookup_field= 'id'
    queryset= User.objects.all()
