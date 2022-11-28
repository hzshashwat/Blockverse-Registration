from django.urls import path, include
from registration_portal.views import *

app_name = 'registration_portal'

urlpatterns = [
    path('registration/', LandingPageView.as_view(), name='landingpage'),
    path('register/google-oauth/', RegistrationGoogleOAuthView.as_view(), name='registration_google-oauth'),

]
