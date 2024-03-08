# Generated by Django 5.0.2 on 2024-02-29 20:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0014_profile_location_profile_pets'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='user_years',
            field=models.CharField(choices=[('inbound', 'Inbound Novo'), ('current', 'Current Novo'), ('alum', 'Novo Alum')], default='inbound', max_length=10),
        ),
    ]
