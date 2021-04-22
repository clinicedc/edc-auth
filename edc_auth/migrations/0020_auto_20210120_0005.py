# Generated by Django 3.0.9 on 2021-01-19 21:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("edc_auth", "0019_userprofile_export_format"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="role",
            options={
                "default_permissions": (
                    "add",
                    "change",
                    "delete",
                    "view",
                    "export",
                    "import",
                ),
                "get_latest_by": "modified",
                "ordering": ["display_index", "display_name"],
            },
        ),
    ]