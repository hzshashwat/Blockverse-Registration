from django.urls import path, include
from registration_portal.views import *

app_name = 'registration_portal'

urlpatterns = [
    path('registration/', LandingPageView.as_view(), name='landingpage'),
    path('register/google-oauth/', RegistrationGoogleOAuthView.as_view(), name='registration_google-oauth'),
    path('register/fill-details/', FillDetailsView.as_view(), name='filldetails'),
    path('error/email_notallowed/', EmailNotAllowedView.as_view(), name='emailnotallowederror'),
    path('register/payment/', PaymentPageView.as_view(), name='paymentpage'),
    path('register/confirm/<payment_id>/<order_id>/<signature>/', ConfirmRegistration.as_view(), name='confirmregistration')
]
