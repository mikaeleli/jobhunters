# Generated by Django 4.2.11 on 2024-05-07 22:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("job_hunters", "0003_remove_image_image_alter_job_posted_date"),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="full_name",
            field=models.CharField(blank=True, max_length=255),
        ),
    ]