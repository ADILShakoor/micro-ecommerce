# Generated by Django 4.1.13 on 2024-09-20 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purchases', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase',
            name='stripe_checkout_session_id',
            field=models.CharField(blank=True, max_length=220, null=True),
        ),
    ]
