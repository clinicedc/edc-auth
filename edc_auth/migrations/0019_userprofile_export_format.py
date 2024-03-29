# Generated by Django 3.0.9 on 2020-10-02 01:03

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("edc_auth", "0018_auto_20191029_2039"),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="export_format",
            field=models.CharField(
                blank=True,
                choices=[
                    ("CSV", "CSV (delimited by pipe `|`"),
                    (114, "Stata v10 or later"),
                    (117, "Stata v13 or later"),
                    (118, "Stata v14 or later"),
                    (119, "Stata v15 or later"),
                ],
                default="CSV",
                help_text="Note: requires export permissions",
                max_length=25,
                null=True,
                verbose_name="Export format",
            ),
        ),
    ]
