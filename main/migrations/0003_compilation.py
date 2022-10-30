# Generated by Django 4.1.1 on 2022-10-30 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0002_remove_coub_coub_created_at"),
    ]

    operations = [
        migrations.CreateModel(
            name="Compilation",
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
                ("file", models.CharField(blank=True, max_length=300, null=True)),
                ("is_tg_uploaded", models.BooleanField(default=False)),
                ("is_yt_uploaded", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]