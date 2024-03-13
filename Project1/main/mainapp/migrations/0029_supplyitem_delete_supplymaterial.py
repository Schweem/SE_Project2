# Generated by Django 5.0.2 on 2024-03-10 18:51

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("mainapp", "0028_supplymaterial"),
    ]

    operations = [
        migrations.CreateModel(
            name="supplyItem",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("link", models.URLField(blank=True, null=True)),
                ("purchased", models.BooleanField(default=False)),
            ],
        ),
        migrations.DeleteModel(
            name="supplyMaterial",
        ),
    ]
