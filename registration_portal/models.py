from django.db import models
from django.contrib.auth.models import User

class Team(models.Model):
    leader = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    leader_email = models.EmailField(max_length=100)
    leader_profilephoto_url = models.CharField(max_length=150)
    team_name = models.CharField(max_length=100)
    team_member_one = models.CharField(max_length=100)
    team_member_two = models.CharField(max_length=100)
    registration_completed = models.BooleanField(default=False)

class Transaction(models.Model):
    client = models.CharField(max_length=100)
    STATUS_CHOICES = [
        ('S', 'Successful'),
        ('F', 'Failed'),
    ]
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='F')
    razor_pay_order_id = models.CharField(max_length=100, primary_key=True, default='Old')
    razor_pay_payment_id = models.CharField(max_length=100, null=True, blank=True)
    error_code = models.CharField(max_length=100, null=True, blank=True)
    error_description = models.CharField(max_length=100, null=True, blank=True)
    error_reason = models.CharField(max_length=100, null=True, blank=True)