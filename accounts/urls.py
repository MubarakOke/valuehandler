from django.urls import path
from accounts.views import RegistrationView,UserListView,EditUserRoleView, AuthenticateAdminView, AuthenticateSuperAdminView

app_name= 'accounts'

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('auth/superadmin/', AuthenticateSuperAdminView.as_view(), name='auth_superadmin'),
    path('auth/admin/', AuthenticateAdminView.as_view(), name='auth_admin'),
    path('users/',UserListView.as_view(),name='list_users'),
    path('edit/',EditUserRoleView.as_view(),name='edit_role'),
]