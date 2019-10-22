# Generated by Django 2.2.6 on 2019-10-22 01:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("edc_auth", "0008_auto_20191022_0134")]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="alternate_email",
            field=models.EmailField(
                blank=True, max_length=254, verbose_name="Alternate email address"
            ),
        )
    ]
