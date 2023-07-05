# Generated by Django 4.2.1 on 2023-07-05 02:16

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("edc_auth", "0027_alter_edcpermissions_options"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="role",
            options={
                "default_manager_name": "objects",
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
