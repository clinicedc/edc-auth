import sys
from copy import deepcopy
from typing import Optional

from django.apps import apps as django_apps
from django.utils.module_loading import import_module, module_has_submodule


class AlreadyRegistered(Exception):
    pass


class SiteAuthError(Exception):
    pass


class SiteAuths:
    def __init__(self):
        self.registry = {"groups": {}, "roles": {}}

    def register(
        self,
        groups: Optional[dict] = None,
        roles: Optional[dict] = None,
    ):
        for group_name, codenames in groups.items():
            self.add_or_update_group(group_name, codenames)

        for role_name, group_names in roles.items():
            self.add_or_update_role(role_name, group_names)

    def add_or_update_role(self, role_name: str, group_names: list, replace=None):
        """Adds to or replaces group names associated with this role name.

        Gurantees the resulting group names list for the role is unique"""
        if replace:
            group_names = list(set(group_names))
            self.registry["roles"].update({role_name: group_names})
        else:
            existing_group_names = deepcopy(self.registry["roles"].get(role_name)) or []
            existing_group_names.extend(group_names)
            existing_group_names = list(set(existing_group_names))
            self.registry["roles"].update({role_name: existing_group_names})
        return self.registry["roles"].get(role_name)

    def add_or_update_group(self, group_name: str, codenames: list, replace=None):
        """Adds to or replaces codenames associated with this group name.

        Gurantees the resulting codenames list is unique"""
        if replace:
            codenames = list(set(codenames))
            self.registry["groups"].update({group_name: codenames})
        else:
            existing_codenames = deepcopy(self.registry["groups"].get(group_name)) or []
            existing_codenames.extend(codenames)
            existing_codenames = list(set(existing_codenames))
            self.registry["groups"].update({group_name: existing_codenames})
        return self.registry["groups"].get(group_name)

    @property
    def roles(self):
        return self.registry["roles"]

    @property
    def groups(self):
        return self.registry["groups"]

    @staticmethod
    def autodiscover(module_name=None, verbose=True):
        """Autodiscovers in the auths.py file of any INSTALLED_APP."""
        before_import_registry = None
        module_name = module_name or "auths"
        writer = sys.stdout.write if verbose else lambda x: x
        writer(f" * checking for site {module_name} ...\n")
        for app in django_apps.app_configs:
            writer(f" * searching {app}           \r")
            try:
                mod = import_module(app)
                try:
                    before_import_registry = deepcopy(site_auths.registry)
                    import_module(f"{app}.{module_name}")
                    writer(f" * registered '{module_name}' from '{app}'\n")
                except ImportError as e:
                    site_auths.registry = before_import_registry
                    if module_has_submodule(mod, module_name):
                        raise SiteAuthError(str(e))
            except ImportError:
                pass


site_auths = SiteAuths()
