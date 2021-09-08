import sys

from django.apps import AppConfig as DjangoAppConfig
from django.core.checks.registry import register
from django.core.management.color import color_style
from django.db.models.signals import post_migrate

from .auth_updater import AuthUpdater
from .system_checks import edc_check

style = color_style()


def post_migrate_user_groups_and_roles(sender=None, **kwargs):  # noqa
    """Update Groups, Role model with EDC defaults."""
    from django.apps import apps as django_apps

    AuthUpdater(apps=django_apps, verbose=True)


class AppConfig(DjangoAppConfig):
    name = "edc_auth"
    verbose_name = "Edc Authentication"

    def ready(self):
        from .site_auths import site_auths

        sys.stdout.write(f"Loading {self.verbose_name} ...\n")
        site_auths.autodiscover()
        post_migrate.connect(post_migrate_user_groups_and_roles, sender=self)
        register(edc_check)
        sys.stdout.write(f" Done loading {self.verbose_name}.\n")
