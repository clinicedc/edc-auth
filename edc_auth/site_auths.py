import sys
from copy import deepcopy
from typing import Optional

from django.apps import apps as django_apps
from django.utils.module_loading import import_module, module_has_submodule


class AlreadyRegistered(Exception):
    pass


class InvalidGroup(Exception):
    pass


class InvalidRole(Exception):
    pass


class RoleAlreadyExists(Exception):
    pass


class GroupAlreadyExists(Exception):
    pass


class SiteAuthError(Exception):
    pass


class SiteAuths:
    """A global to hold the intended group and role data.

    Data here will be used by AuthUpdater.
    """

    def __init__(self):
        self.registry = {
            "groups": {},
            "roles": {},
            "post_update_funcs": [],
            "pii_models": [],
        }
        self.loaded = False

    def register(
        self,
        groups: Optional[dict] = None,
        roles: Optional[dict] = None,
        pii_models: Optional[list] = None,
        post_update_funcs: Optional[list] = None,
    ):
        if self.loaded:
            raise SiteAuthError(
                "Already registered. `register` may only be called once. "
                "Try the add/update/replace methods."
            )
        self.add_groups(groups)
        self.add_roles(roles)
        self.registry["post_update_funcs"] = post_update_funcs or []
        self.registry["pii_models"] = pii_models or []
        self.loaded = True

    def add_post_update_func(self, func):
        self.registry["post_update_funcs"].append(func)

    def add_pii_model(self, model_name):
        self.registry["pii_models"].append(model_name)

    def add_groups(self, data: dict):
        for name, codenames in data.items():
            self.add_group(name, codenames)

    def add_roles(self, data: dict):
        for name, group_names in data.items():
            self.add_role(name, group_names)

    def add_group(self, name, codenames_or_func):
        if name in self.registry["groups"]:
            raise GroupAlreadyExists(f"Group name already exists. Got {name}.")
        self.registry["groups"].update({name: codenames_or_func})

    def add_role(self, name, group_names):
        if name in self.registry["groups"]:
            raise RoleAlreadyExists(f"Role name already exists. Got {name}.")
        group_names = list(set(group_names))
        self.registry["roles"].update({name: group_names})

    def update_group(self, name: str, codenames: list) -> None:
        codenames = list(set(codenames))
        if name not in self.registry["groups"]:
            raise InvalidGroup(f"Unable to update. Invalid group name. Got {name}")
        existing_codenames = deepcopy(self.registry["groups"].get(name)) or []
        existing_codenames.extend(codenames)
        existing_codenames = list(set(existing_codenames))
        self.registry["groups"].update({name: existing_codenames})

    def update_role(self, name: str, group_names: list) -> None:
        group_names = list(set(group_names))
        if name not in self.registry["roles"]:
            raise InvalidRole(f"Unable to update. Invalid role name. Got {name}")
        existing_group_names = deepcopy(self.registry["roles"].get(name)) or []
        existing_group_names.extend(group_names)
        existing_group_names = list(set(existing_group_names))
        self.registry["roles"].update({name: existing_group_names})

    def replace_group(self, name, codenames):
        del self.registry["groups"][name]
        self.add_group(name, codenames)

    def replace_role(self, name, group_names):
        del self.registry["roles"][name]
        self.add_role(name, group_names)

    @property
    def roles(self):
        return self.registry["roles"]

    @property
    def groups(self):
        return self.registry["groups"]

    @property
    def post_update_funcs(self):
        return self.registry["post_update_funcs"]

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
