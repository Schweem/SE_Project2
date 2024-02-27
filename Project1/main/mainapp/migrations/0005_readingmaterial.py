# Generated by Django 5.0.2 on 2024-02-15 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0004_rename_todolist_event'),
    ]

    operations = [
        migrations.CreateModel(
            name='readingMaterial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('author', models.CharField(max_length=100)),
                ('type', models.CharField(max_length=100)),
                ('link', models.URLField()),
                ('read', models.BooleanField(default=False)),
            ],
        ),
    ]
