# Generated by Django 3.2.13 on 2022-08-24 21:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("edc_auth", "0025_permissions"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Permissions",
            new_name="EdcPermissions",
        ),
    ]
