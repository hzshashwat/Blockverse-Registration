# Generated by Django 4.1.3 on 2022-12-02 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration_portal', '0003_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client', models.CharField(max_length=100)),
                ('razor_pay_order_id', models.CharField(max_length=100)),
                ('razor_pay_payment_id', models.CharField(max_length=100)),
                ('razor_pay_payment_signature', models.CharField(max_length=100)),
                ('status', models.BooleanField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='team',
            name='registration_completed',
            field=models.BooleanField(default=False),
        ),
    ]