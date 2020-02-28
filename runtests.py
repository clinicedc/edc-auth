#!/usr/bin/env python
import django
import logging
import os
import sys

from django.conf import settings
from django.test.runner import DiscoverRunner
from edc_test_utils import DefaultTestSettings
from os.path import abspath, dirname

app_name = "edc_auth"
base_dir = dirname(abspath(__file__))

DEFAULT_SETTINGS = DefaultTestSettings(
    calling_file=__file__,
    BASE_DIR=base_dir,
    APP_NAME=app_name,
    ETC_DIR=os.path.join(base_dir, app_name, "tests", "etc"),
    EDC_NAVBAR_DEFAULT="edc_auth",
    EDC_BOOTSTRAP=3,
    INSTALLED_APPS=[
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
        "django.contrib.sites",
        "django_celery_results",
        "django_celery_beat",
        "logentry_admin",
        "django_crypto_fields.apps.AppConfig",
        "edc_action_item.apps.AppConfig",
        "adverse_event_app.apps.AppConfig",
        "edc_adverse_event.apps.AppConfig",
        "edc_randomization.apps.AppConfig",
        "edc_appointment.apps.AppConfig",
        "edc_list_data.apps.AppConfig",
        "edc_auth.apps.AppConfig",
        "edc_dashboard.apps.AppConfig",
        "edc_data_manager.apps.AppConfig",
        "edc_device.apps.AppConfig",
        "edc_export.apps.AppConfig",
        "edc_identifier.apps.AppConfig",
        "edc_lab.apps.AppConfig",
        "edc_lab_dashboard.apps.AppConfig",
        "edc_locator.apps.AppConfig",
        "edc_metadata.apps.AppConfig",
        "edc_metadata_rules.apps.AppConfig",
        "edc_navbar.apps.AppConfig",
        "edc_notification.apps.AppConfig",
        "edc_offstudy.apps.AppConfig",
        "edc_pharmacy.apps.AppConfig",
        "edc_reference.apps.AppConfig",
        "edc_registration.apps.AppConfig",
        "edc_sites.apps.AppConfig",
        "edc_visit_schedule.apps.AppConfig",
    ],
    add_dashboard_middleware=True,
    add_lab_dashboard_middleware=True,
    use_test_urls=True,
).settings


def main():
    if not settings.configured:
        settings.configure(**DEFAULT_SETTINGS)
    django.setup()
    tags = [t.split("=")[1] for t in sys.argv if t.startswith("--tag")]
    failures = DiscoverRunner(failfast=False, tags=tags).run_tests(
        [f"{app_name}.tests"]
    )
    sys.exit(failures)


if __name__ == "__main__":
    logging.basicConfig()
    main()
