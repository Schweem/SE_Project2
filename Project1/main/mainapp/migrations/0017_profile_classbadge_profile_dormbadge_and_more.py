# Generated by Django 5.0.2 on 2024-03-03 03:42

import mainapp.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0016_profile_interests_alter_event_url_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='classBadge',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='profile',
            name='dormBadge',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='profile',
            name='eventsBadge',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='profile',
            name='facultyBadge',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='profile',
            name='hamBadge',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='profile',
            name='profile_picture',
            field=models.ImageField(blank=True, default='userprofiles/default.jpg', null=True, upload_to=mainapp.models.Profile.user_directory_path),
        ),
        migrations.AlterField(
            model_name='profile',
            name='user_years',
            field=models.CharField(choices=[('Inbound', 'Inbound Novo'), ('Current', 'Current Novo'), ('Alum', 'Novo Alum')], default='inbound', max_length=20),
        ),
    ]
