# Generated by Django 5.0.2 on 2024-03-05 03:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0017_profile_classbadge_profile_dormbadge_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='readingmaterial',
            name='author',
        ),
        migrations.RemoveField(
            model_name='readingmaterial',
            name='link',
        ),
        migrations.RemoveField(
            model_name='readingmaterial',
            name='type',
        ),
    ]
