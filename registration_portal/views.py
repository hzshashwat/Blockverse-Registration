from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class LandingPageView(View):
    def get(self, request):
        return render(request, 'registration_portal/landing_page.html')

class RegistrationGoogleOAuthView(View):
    def get(self, request):
        return render(request, 'registration_portal/google_oauth.html')

class FillDetailsView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'registration_portal/fill_details.html')
        