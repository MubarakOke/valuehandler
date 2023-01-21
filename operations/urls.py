from django.urls import path
from .views import RateView, RateDetailView, TariffView, TariffDetailView, CalculationView, RateTariffView

app_name= 'operations'

urlpatterns = [
    path('rate/', RateView.as_view(), name='rate_create_list'),
    path('rate/<id>/', RateDetailView.as_view(), name='rate_update'),
    path('tariff/', TariffView.as_view(), name='tariff_upload'),
    path('tariff/<hscode>/', TariffDetailView.as_view(), name='tariff_update'),
    path('calculation/', CalculationView.as_view(), name='calculate_create_list'),
    path('data/', RateTariffView.as_view(), name='rate_tariff_list')
]