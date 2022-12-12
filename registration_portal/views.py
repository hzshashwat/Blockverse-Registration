from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from social_django.models import UserSocialAuth
from django.contrib.auth.models import User
from django.contrib.auth import logout
from registration_portal.models import Team, Transaction
from registration_portal.forms import TeamForm
import requests
import razorpay
from django.conf import settings

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

# Create your views here.
current_domain = 'http://127.0.0.1:8000'

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
            
            try:
                Token = entry_auth.access_token
                APIKey = 'AIzaSyAHzddem3jEoQVlls4ES2nos7IcNHr5Wqk'
                params = {"personFields" : "photos", "key" : APIKey}
                headers={'Authorization':f'Bearer {Token}'}
                r = requests.get('https://people.googleapis.com/v1/people/me', params= params, headers= headers)
                rjson=r.json()
                photourl = list(rjson['photos'])[0]['url']
            except:
                pass
            
            try:
                team = Team.objects.get(leader_email = email)
            except:
                entry_details = Team(
                leader = entry_user,
                leader_email = email,
                leader_profilephoto_url = photourl,
                )
                entry_details.save()
                team = Team.objects.get(leader_email = email)

            if team.registration_completed == True:
                return redirect(reverse('registration_portal:alreadyregistered'))
            else:
                form = TeamForm()
                return render(request, 'registration_portal/fill_details.html', context={"form" : form})
        else:
            entry_auth.delete()
            entry_user.delete()
            return redirect(reverse('registration_portal:emailnotallowederror'))

    def post(self, request):
        email = request.user.email
        entry_auth = UserSocialAuth.objects.filter(provider="google-oauth2").get(uid=email)
        logged_user = User.objects.get(email = email)

        # team_profilephoto = request.POST['team_profilephoto']
        team_name = request.POST['team_name']
        # team_member_profilephoto = request.POST['team_member_profilephoto']
        team_member_name = request.POST['team_member_name']
        team_member_email = request.POST['team_member_email']

        entry_details = Team.objects.get(leader = logged_user)
        # entry_details.team_profilephoto = team_profilephoto
        entry_details.team_name = team_name
        # entry_details.team_member_profilephoto = team_member_profilephoto
        entry_details.team_member_name = team_member_name
        entry_details.team_member_email = team_member_email
        entry_details.save()
        
        team = Team.objects.get(leader_email = email)
        if team.payment_completed == True:
            return redirect(reverse('registration_portal:confirmregistration'))
        else:
            return redirect(reverse('registration_portal:paymentpage'))

class PaymentPageView(LoginRequiredMixin, View):
    def get(self, request):
        key = settings.RAZORPAY_KEY_ID
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        order = client.order.create({"amount" : 2000, "currency" : "INR", "payment_capture" : 1})
        context = {'order' : order, 'key' : key, 'current_domain' : current_domain}

        email = request.user.email
        team = Team.objects.get(leader_email = email)
        if team.registration_completed == True:
            return redirect(reverse('registration_portal:alreadyregistered'))
        elif team.payment_completed == True:
            return redirect(reverse('registration_portal:confirmregistration'))
        else:
            orderid = Transaction(
                client_email = request.user.email,
                razor_pay_order_id = order['id'],
            )
            orderid.save()

            return render(request, 'registration_portal/payment_page.html', context)

class PaymentSuccess(LoginRequiredMixin, View):
    def get(self, request, payment_id, order_id, signature):
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        
        try:
            client.utility.verify_payment_signature({
            'razorpay_order_id': order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
            })
            payment = Transaction.objects.get(razor_pay_order_id = order_id)
            payment.razor_pay_payment_id = payment_id
            payment.status = 'S'
            payment.save()

            email = request.user.email
            team = Team.objects.get(leader_email = email)
            team.payment_completed = True
            team.save()

            # ------------- Sending Payment Success Mail ------------- #
            # ---------- For client ---------- #
            team_name = team.team_name
            subject = "Payment Successful"
            description = "Your payment has been received. Please continue and confirm your registration information to reserve your spot for Blockverse."

            html_content = render_to_string("registration_portal/client_email.html", {'team_name' : team_name, 'description' : description})
            text_content = strip_tags(html_content)

            email = EmailMultiAlternatives(
            subject,
            text_content,
            settings.EMAIL_HOST_USER,
            [email]
            )
            email.attach_alternative(html_content, "text/html")
            email.send()

            # ---------- For admin ---------- #
            subject_admin = f"Payment successful for {team_name}"
            context_admin = {
                'status' : 'Successful',
                'team_name' : team_name,
                'leader_email' : team.leader_email,
                'team_member_name' : team.team_member_name,
                'team_member_email' : team.team_member_email,
                'payment_id' : payment_id,
                'order_id' : order_id,
                'amount' : '20 INR',
                'error_code' : '---',
                'error_reason' : '---',
            }

            html_content_admin = render_to_string("registration_portal/admin_email.html", context_admin)
            text_content_admin = strip_tags(html_content_admin)

            email_admin = EmailMultiAlternatives(
            subject_admin,
            text_content_admin,
            settings.EMAIL_HOST_USER,
            ['shashwatsingh741@gmail.com', ]
            )
            email_admin.attach_alternative(html_content_admin, "text/html")
            email_admin.send()
            # ------------------------------------------------- #

            return redirect(reverse('registration_portal:confirmregistration'))
        except razorpay.errors.SignatureVerificationError:
            return render(request, 'registration_portal/payment_signature_not_found.html')

class PaymentFailed(LoginRequiredMixin, View):
    def get(self, request, payment_id, order_id, error_code, error_description, error_reason):
        payment = Transaction.objects.get(razor_pay_order_id = order_id)
        payment.razor_pay_payment_id = payment_id
        payment.status = 'F'
        payment.error_code = error_code
        payment.error_description = error_description
        payment.error_reason = error_reason
        payment.save()
        context = {'error_description' : error_description}

        # ------------- Sending Payment Success Mail ------------- #
        email = request.user.email
        team = Team.objects.get(leader_email = email)
        team_name = team.team_name
        subject = "Payment Unsuccessful"
        description = error_description

        html_content = render_to_string("registration_portal/client_email.html", {'team_name' : team_name, 'description' : description})
        text_content = strip_tags(html_content)

        email = EmailMultiAlternatives(
        subject,
        text_content,
        settings.EMAIL_HOST_USER,
        [email]
        )
        email.attach_alternative(html_content, "text/html")
        email.send()

        # ---------- For admin ---------- #
        subject_admin = f"Payment unsuccessful for {team_name}"
        context_admin = {
            'status' : 'Failed',
            'team_name' : team_name,
            'leader_email' : team.leader_email,
            'team_member_name' : team.team_member_name,
            'team_member_email' : team.team_member_email,
            'payment_id' : payment_id,
            'order_id' : order_id,
            'error_code' : error_code,
            'error_reason' : error_reason,
            'amount' : '20 INR'
        }

        html_content_admin = render_to_string("registration_portal/admin_email.html", context_admin)
        text_content_admin = strip_tags(html_content_admin)

        email_admin = EmailMultiAlternatives(
        subject_admin,
        text_content_admin,
        settings.EMAIL_HOST_USER,
        ['shashwatsingh741@gmail.com', ]
        )
        email_admin.attach_alternative(html_content_admin, "text/html")
        email_admin.send()
        # ------------------------------------------------- #
        
        return render(request, 'registration_portal/payment_failed.html', context= context)

class ConfirmRegistration(LoginRequiredMixin, View):
    def get(self, request):
        email = request.user.email
        team = Team.objects.get(leader_email = email)
        leader = User.objects.get(email = email)
        context = {'team' : team, 'leader' : leader}
        if team.registration_completed == True:
            return redirect(reverse('registration_portal:alreadyregistered'))
        elif team.payment_completed == True:
            return render(request, 'registration_portal/confirm_registration.html', context=context)
        else:
            return redirect(reverse('registration_portal:paymentpage'))

    def post(self, request):
        email = request.user.email
        team = Team.objects.get(leader_email = email)
        team.registration_completed = True
        team.save()

        # ------------- Sending Payment Success Mail ------------- #
        team_name = team.team_name
        subject = f"{team_name} Registered for Blockverse"
        description = "Thank you for registering for our tech event Blockverse! We are anticipating your participation at the event. Further details regarding the venue and timings will be shared soon on the registered email. Stay Tuned."

        html_content = render_to_string("registration_portal/client_email.html", {'team_name' : team_name, 'description' : description})
        text_content = strip_tags(html_content)

        email = EmailMultiAlternatives(
        subject,
        text_content,
        settings.EMAIL_HOST_USER,
        [email]
        )
        email.attach_alternative(html_content, "text/html")
        email.send()

        # ---------- For admin ---------- #
        subject_admin = f"{team_name} got registered for blockverse"
        context_admin = {
            'status' : 'Registered',
            'team_name' : team_name,
            'leader_email' : team.leader_email,
            'team_member_name' : team.team_member_name,
            'team_member_email' : team.team_member_email,
            'payment_id' : "---",
            'order_id' : "---",
            'error_code' : "---",
            'error_reason' : "---",
            'amount' : "---"
        }

        html_content_admin = render_to_string("registration_portal/admin_email.html", context_admin)
        text_content_admin = strip_tags(html_content_admin)

        email_admin = EmailMultiAlternatives(
        subject_admin,
        text_content_admin,
        settings.EMAIL_HOST_USER,
        ['shashwatsingh741@gmail.com', ]
        )
        email_admin.attach_alternative(html_content_admin, "text/html")
        email_admin.send()
        # ------------------------------------------------- #

        return render(request, 'registration_portal/registration_confirmed.html')

class AlreadyRegistered(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'registration_portal/already_registered.html')