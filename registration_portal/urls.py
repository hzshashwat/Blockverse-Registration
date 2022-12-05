from django.urls import path, include
from registration_portal.views import *
from django.conf.urls.static import static
from django.conf import settings

app_name = 'registration_portal'

urlpatterns = [
    path('registration/', LandingPageView.as_view(), name='landingpage'),
    path('register/google-oauth/', RegistrationGoogleOAuthView.as_view(), name='registration_google-oauth'),
    path('register/fill-details/', FillDetailsView.as_view(), name='filldetails'),
    path('error/email_notallowed/', EmailNotAllowedView.as_view(), name='emailnotallowederror'),
    path('register/payment/', PaymentPageView.as_view(), name='paymentpage'),
    path('register/payment/success/<payment_id>/<order_id>/<signature>/', PaymentSuccess.as_view(), name='paymentsuccess'),
    path('register/confirm/', ConfirmRegistration.as_view(), name='confirmregistration'),
    path('register/payment/failed/<payment_id>/<order_id>/<error_code>/<error_description>/<error_reason>/', PaymentFailed.as_view(), name='paymentfailed'),
    path('register/completed/', AlreadyRegistered.as_view(), name='alreadyregistered')
]
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)