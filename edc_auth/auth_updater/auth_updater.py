import sys
from typing import Optional

from django.core.management.color import color_style

from edc_auth.site_auths import site_auths

from .group_updater import GroupUpdater
from .role_updater import RoleUpdater

style = color_style()


class AuthUpdater:
    group_updater_cls = GroupUpdater
    role_updater_cls = RoleUpdater

    def __init__(
        self,
        groups: Optional[dict] = None,
        roles: Optional[dict] = None,
        post_updates=None,
        verbose=None,
        **kwargs,
    ):
        if verbose:
            sys.stdout.write(
                style.MIGRATE_HEADING("Updating groups and permissions:\n")
            )
        self.group_updater = self.group_updater_cls(
            groups=groups or site_auths.groups, **kwargs
        )
        self.role_updater = self.role_updater_cls(
            roles=roles or site_auths.roles, verbose=None, **kwargs
        )
        self.groups = self.group_updater.update_groups()
        self.roles = self.role_updater.update_roles()
        self.post_update(post_updates, verbose=None, **kwargs)

        if verbose:
            sys.stdout.write(style.MIGRATE_HEADING("Done\n"))
            sys.stdout.flush()

    # def update_group(self, *args, **kwargs):
    #     return self.group_updater.update_group(*args, **kwargs)

    def post_update(self, post_updates, **kwargs):
        """Custom funcs that operate after all groups and roles have been created"""
        groups = self.group_updater.group_model_cls.objects.all()
        roles = self.role_updater.role_model_cls.objects.all()
        for func in post_updates:
            func(self, groups=groups, roles=roles, **kwargs)
