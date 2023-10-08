from django.urls import path
from .views import VerifyCertificateView, GenerateAccessCodeView

urlpatterns = [
    path('verify-certificate/', VerifyCertificateView.as_view(),
         name="verify-certificate"),
    path('generate-access-code/', GenerateAccessCodeView.as_view(),
         name="generate-access-code"),

]
