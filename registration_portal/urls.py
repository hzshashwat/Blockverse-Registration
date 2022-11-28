from django.urls import path, include
from registration_portal.views import *

urlpatterns = [
    path('registration/', LandingPageView.as_view(), name='landingpage')
]
