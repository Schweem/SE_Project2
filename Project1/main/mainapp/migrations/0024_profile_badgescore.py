# Generated by Django 5.0.2 on 2024-03-05 04:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0023_remove_profile_badges'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='badgeScore',
            field=models.IntegerField(default=0),
        ),
    ]
