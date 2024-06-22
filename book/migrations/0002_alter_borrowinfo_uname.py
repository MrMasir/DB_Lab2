# Generated by Django 5.0.6 on 2024-06-12 18:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("book", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="borrowinfo",
            name="uname",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="book.userinfo",
                verbose_name="用户名",
            ),
        ),
    ]