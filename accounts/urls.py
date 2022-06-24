from django.urls import path
from accounts.views import RegistrationView, UserListView,EditUserRoleView, AuthenticateView, UserListView, EditUserRoleView

app_name= 'accounts'

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('auth/', AuthenticateView.as_view(), name='auth'),
    path('user/',UserListView.as_view(),name='list_users'),
    path('user/<int:id>/',EditUserRoleView.as_view(),name='edit_role'),
]