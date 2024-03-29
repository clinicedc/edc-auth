from django.conf import settings

if (
    "django_celery_beat" in settings.INSTALLED_APPS
    or "django_celery_beat.apps.AppConfig" in settings.INSTALLED_APPS
):
    celery_manager = [
        "django_celery_beat.add_clockedschedule",
        "django_celery_beat.add_crontabschedule",
        "django_celery_beat.add_intervalschedule",
        "django_celery_beat.add_periodictask",
        "django_celery_beat.add_periodictasks",
        "django_celery_beat.add_solarschedule",
        "django_celery_beat.change_clockedschedule",
        "django_celery_beat.change_crontabschedule",
        "django_celery_beat.change_intervalschedule",
        "django_celery_beat.change_periodictask",
        "django_celery_beat.change_periodictasks",
        "django_celery_beat.change_solarschedule",
        "django_celery_beat.delete_clockedschedule",
        "django_celery_beat.delete_crontabschedule",
        "django_celery_beat.delete_intervalschedule",
        "django_celery_beat.delete_periodictask",
        "django_celery_beat.delete_periodictasks",
        "django_celery_beat.delete_solarschedule",
        "django_celery_beat.view_clockedschedule",
        "django_celery_beat.view_crontabschedule",
        "django_celery_beat.view_intervalschedule",
        "django_celery_beat.view_periodictask",
        "django_celery_beat.view_periodictasks",
        "django_celery_beat.view_solarschedule",
        "django_celery_results.add_taskresult",
        "django_celery_results.change_taskresult",
        "django_celery_results.delete_taskresult",
        "django_celery_results.view_taskresult",
    ]
else:
    celery_manager = []

if (
    "django_celery_results" in settings.INSTALLED_APPS
    or "django_celery_results.apps.AppConfig" in settings.INSTALLED_APPS
):
    celery_manager.extend(
        [
            "django_celery_results.add_taskresult",
            "django_celery_results.change_taskresult",
            "django_celery_results.delete_taskresult",
            "django_celery_results.view_taskresult",
        ]
    )
