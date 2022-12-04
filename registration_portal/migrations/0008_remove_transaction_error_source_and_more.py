# Generated by Django 4.1.3 on 2022-12-04 10:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration_portal', '0007_remove_transaction_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='error_source',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='error_step',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='razor_pay_payment_signature',
        ),
        migrations.AlterField(
            model_name='transaction',
            name='status',
            field=models.CharField(choices=[('S', 'Successful'), ('F', 'Failed')], default='F', max_length=1),
        ),
    ]
