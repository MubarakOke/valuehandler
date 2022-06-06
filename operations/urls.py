from django.urls import path
from .views import RateView, RateDetailView, EditUserRoleView,UserListView,TariffView, TariffDetailView, CalculationView

app_name= 'operations'

urlpatterns = [
    path('rate/', RateView.as_view(), name='rate_create_list'),
    path('rate/<int:id>/', RateDetailView.as_view(), name='rate_update'),
    path('tariff/', TariffView.as_view(), name='tariff_upload'),
    path('tariff/<int:id>/', TariffDetailView.as_view(), name='tariff_update'),
    path('calculation/', CalculationView.as_view(), name='calculate_create_list'),
]