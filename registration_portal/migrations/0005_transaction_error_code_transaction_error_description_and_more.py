# Generated by Django 4.1.3 on 2022-12-02 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration_portal', '0004_transaction_team_registration_completed'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='error_code',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='transaction',
            name='error_description',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='transaction',
            name='error_reason',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='transaction',
            name='error_source',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='transaction',
            name='error_step',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='razor_pay_order_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='razor_pay_payment_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='razor_pay_payment_signature',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]