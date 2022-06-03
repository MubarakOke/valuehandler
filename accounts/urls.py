from django.urls import path
from accounts.views import RegistrationView, AuthenticateAdminView, AuthenticateSuperAdminView

app_name= 'accounts'

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('auth/superadmin/', AuthenticateSuperAdminView.as_view(), name='auth_superadmin'),
    path('auth/admin/', AuthenticateAdminView.as_view(), name='auth_admin'),
]