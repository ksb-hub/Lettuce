# Generated by Django 4.2.3 on 2023-08-15 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ImageConverters", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="comparelist",
            name="aspects",
            field=models.CharField(default=["11"], max_length=200),
        ),
    ]
