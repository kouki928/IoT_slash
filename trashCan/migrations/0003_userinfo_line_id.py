# Generated by Django 4.1.4 on 2023-06-23 01:01

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("trashCan", "0002_usernotice"),
    ]

    operations = [
        migrations.AddField(
            model_name="userinfo",
            name="line_id",
            field=models.CharField(default=django.utils.timezone.now, max_length=100),
            preserve_default=False,
        ),
    ]
