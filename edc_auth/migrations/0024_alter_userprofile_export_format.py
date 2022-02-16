# Generated by Django 3.2.8 on 2022-02-15 21:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('edc_auth', '0023_auto_20210423_1451'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='export_format',
            field=models.CharField(blank=True, choices=[('CSV', 'CSV (delimited by pipe `|`)'), (114, 'Stata v10 or later'), (117, 'Stata v13 or later'), (118, 'Stata v14 or later'), (119, 'Stata v15 or later')], default='CSV', help_text='Note: requires export permissions', max_length=25, null=True, verbose_name='Export format'),
        ),
    ]
