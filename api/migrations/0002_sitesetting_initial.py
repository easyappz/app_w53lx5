from django.db import migrations


def create_initial_setting(apps, schema_editor):
    SiteSetting = apps.get_model('api', 'SiteSetting')
    if not SiteSetting.objects.exists():
        SiteSetting.objects.create(header_title='Авитолог')


def reverse_initial_setting(apps, schema_editor):
    SiteSetting = apps.get_model('api', 'SiteSetting')
    # keep settings, do nothing on reverse


class Migration(migrations.Migration):
    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_initial_setting, reverse_initial_setting),
    ]
