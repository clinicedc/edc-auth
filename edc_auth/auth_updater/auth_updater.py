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
        pii_models: Optional[dict] = None,
        post_update_funcs=None,
        verbose=None,
        apps=None,
        **kwargs,
    ):
        self.verbose = verbose
        self.apps = apps
        if self.verbose:
            sys.stdout.write(
                style.MIGRATE_HEADING("Updating groups and permissions:\n")
            )
        self.group_updater = self.group_updater_cls(
            groups=groups or site_auths.groups,
            pii_models=pii_models,
            verbose=self.verbose,
            apps=self.apps,
            **kwargs,
        )
        self.role_updater = self.role_updater_cls(
            roles=roles or site_auths.roles,
            verbose=self.verbose,
            apps=self.apps,
            **kwargs,
        )
        self.groups = self.group_updater.update_groups()
        self.roles = self.role_updater.update_roles()
        self.run_post_updates(post_update_funcs or site_auths.post_update_funcs)
        if verbose:
            sys.stdout.write(style.MIGRATE_HEADING("Done\n"))
            sys.stdout.flush()

    def run_post_updates(self, post_updates):
        """Custom funcs that operate after all groups and roles have been created"""
        if self.verbose:
            sys.stdout.write(style.MIGRATE_HEADING(" - Running post updates:\n"))
        if post_updates:
            for func in post_updates:
                sys.stdout.write(f"   * {func.__name__}\n")
                func(self)
        else:
            sys.stdout.write("   * nothing to do\n")
        if self.verbose:
            sys.stdout.write("   Done\n")

    def create_permissions_from_tuples(self, **kwargs):
        return self.group_updater.create_permissions_from_tuples(**kwargs)

    @property
    def group_model_cls(self):
        return self.group_updater.group_model_cls

    def remove_permissions_by_codenames(self, **kwargs):
        return self.group_updater.remove_permissions_by_codenames(**kwargs)
