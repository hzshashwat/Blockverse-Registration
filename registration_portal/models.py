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
    razor_pay_order_id = models.CharField(max_length=100)
    razor_pay_payment_id = models.CharField(max_length=100)
    razor_pay_payment_signature = models.CharField(max_length=100)
    status = models.BooleanField(max_length=100)