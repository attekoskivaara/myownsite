# Generated by Django 4.2.9 on 2024-01-17 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0008_textin"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="content",
            field=models.TextField(blank=True, null=True),
        ),
    ]
