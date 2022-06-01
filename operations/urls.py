from django.urls import path
from .views import RateUploadView, RateListView, TariffUploadView

app_name= 'operations'

urlpatterns = [
    path('rate/', RateUploadView.as_view(), name='rate_upload'),
    path('rate/list/', RateListView.as_view(), name='rate_upload'),
    path('tariff/', TariffUploadView.as_view(), name='tariff_upload'),
]