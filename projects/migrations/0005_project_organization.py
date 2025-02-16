# Generated by Django 5.1.5 on 2025-02-16 00:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0003_delete_organizationmembership'),
        ('projects', '0004_alter_project_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='organization',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='organizations.organization'),
        ),
    ]
