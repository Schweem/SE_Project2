# Generated by Django 5.0.2 on 2024-03-16 03:38

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0034_supply_usersupply_delete_supplyitem'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='usersupply',
            unique_together={('user', 'supply')},
        ),
    ]