from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from social_django.models import UserSocialAuth
from django.contrib.auth.models import User
from django.contrib.auth import logout
import requests

# Create your views here.
class LandingPageView(View):
    def get(self, request):
        return render(request, 'registration_portal/landing_page.html')

class RegistrationGoogleOAuthView(View):
    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
        return render(request, 'registration_portal/google_oauth.html')

class EmailNotAllowedView(View):
    def get(self, request):
        return render(request, 'registration_portal/email_notallowed.html')

class FillDetailsView(LoginRequiredMixin, View):
    def get(self, request):
        email = request.user.email
        domain = email.split("@")[-1]
        entry_auth = UserSocialAuth.objects.filter(provider="google-oauth2").get(uid=email)
        entry_user = User.objects.get(email = email)

        Token = entry_auth.access_token
        APIKey = 'AIzaSyAHzddem3jEoQVlls4ES2nos7IcNHr5Wqk'
        params = {"personFields" : "photos", "key" : APIKey}
        headers={'Authorization':f'Bearer {Token}'}
        r = requests.get('https://people.googleapis.com/v1/people/me', params= params, headers= headers)
        rjson=r.json()
        photourl = list(rjson['photos'])[0]['url']
        print(photourl)

        if domain == 'akgec.ac.in':
            return render(request, 'registration_portal/fill_details.html')
        else:
            entry_auth.delete()
            entry_user.delete()
            return redirect(reverse('registration_portal:emailnotallowederror'))

