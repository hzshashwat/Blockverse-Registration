from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from social_django.models import UserSocialAuth
from django.contrib.auth.models import User
from django.contrib.auth import logout
from registration_portal.models import Team
from registration_portal.forms import TeamForm
import requests
import razorpay
from django.conf import settings

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

        if domain == 'akgec.ac.in':
            form = TeamForm()
            return render(request, 'registration_portal/fill_details.html', context={"form" : form})
        else:
            entry_auth.delete()
            entry_user.delete()
            return redirect(reverse('registration_portal:emailnotallowederror'))

    def post(self, request):
        form = TeamForm()
        email = request.user.email
        entry_auth = UserSocialAuth.objects.filter(provider="google-oauth2").get(uid=email)
        logged_user = User.objects.get(email = email)

        team_name = request.POST['team_name']
        team_member_one = request.POST['team_member_one']
        pasteam_member_two = request.POST['team_member_two']

        Token = entry_auth.access_token
        APIKey = 'AIzaSyAHzddem3jEoQVlls4ES2nos7IcNHr5Wqk'
        params = {"personFields" : "photos", "key" : APIKey}
        headers={'Authorization':f'Bearer {Token}'}
        r = requests.get('https://people.googleapis.com/v1/people/me', params= params, headers= headers)
        rjson=r.json()
        photourl = list(rjson['photos'])[0]['url']

        entry_details = Team(
            leader = logged_user,
            leader_email = email,
            leader_profilephoto_url = photourl,
            team_name = team_name,
            team_member_one = team_member_one,
            team_member_two = pasteam_member_two
        )
        entry_details.save()
        return redirect(reverse('registration_portal:paymentpage'))

class PaymentPageView(View):
    def get(self, request):
        key = settings.RAZORPAY_KEY_ID
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        order = client.order.create({"amount" : 2000, "currency" : "INR", "payment_capture" : 1})
        context = {'order' : order, 'key' : key}
        print(order)
        return render(request, 'registration_portal/payment_page.html', context)