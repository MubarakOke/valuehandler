from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User= get_user_model()

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'access': str(refresh.access_token),
    }

class UserSerializer(serializers.ModelSerializer):
    password= serializers.CharField(write_only=True, required=False)
    token= serializers.SerializerMethodField(read_only=True)
    class Meta:
        model= User
        fields= [
            'email',
            'user_type',
            'password',
            'token'
        ]

    def get_token(self, obj):
        user= obj.user
        token= get_tokens_for_user(user)
        return token["access"]
