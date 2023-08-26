from django.urls import path
from .views import VerifyCertificateView

urlpatterns = [
     path('verify-certificate/', VerifyCertificateView.as_view(), name="verify-certificate"),
]
