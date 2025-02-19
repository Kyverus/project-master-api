# Generated by Django 5.1.5 on 2025-02-06 09:11

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='organizationmembership',
            name='admin',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='organizationmembership',
            name='date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='organizationmembership',
            name='owner',
            field=models.BooleanField(default=False),
        ),
    ]
