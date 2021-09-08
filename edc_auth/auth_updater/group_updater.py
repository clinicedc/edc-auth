import sys
from typing import Optional
from warnings import warn

from django.apps import apps as django_apps
from django.conf import settings
from django.core.exceptions import (
    MultipleObjectsReturned,
    ObjectDoesNotExist,
    ValidationError,
)
from django.core.management.color import color_style

from ..default_group_names import PII, PII_VIEW

style = color_style()


class PermissionsCodenameError(Exception):
    pass


class PermissionsCreatorError(ValidationError):
    pass


class CodenameDoesNotExist(Exception):
    pass


INVALID_APP_LABEL = "invalid_app_label"
EDC_AUTH_CODENAMES_WARN_ONLY = getattr(settings, "EDC_AUTH_CODENAMES_WARN_ONLY", False)


class GroupUpdater:
    def __init__(
        self,
        groups: Optional[dict] = None,
        apps=None,
        verbose=None,
        pii_models=None,
        **kwargs,
    ):
        self.apps = apps or django_apps
        self.groups = groups
        self.group_names = list(self.groups.keys())
        self.verbose = verbose
        self.pii_models = pii_models or []
        self.group_model_cls = self.apps.get_model("auth.group")
        self.permission_model_cls = self.apps.get_model("auth.permission")
        self.content_type_model_cls = self.apps.get_model("contenttypes.contenttype")

    def update_groups(self):
        if self.verbose:
            sys.stdout.write(style.MIGRATE_HEADING(" - Updating groups:\n"))
        for group_name, codenames in self.groups.items():
            self.update_group(group_name, codenames, create_group=True)
        for group in self.group_model_cls.objects.exclude(name__in=[PII, PII_VIEW]):
            self.remove_pii_permissions_from_group(group)
        self.group_model_cls.objects.exclude(name__in=self.group_names).delete()
        if self.verbose:
            sys.stdout.write("   Done.\n")

    def update_group(self, group_name, codenames, create_group=None):
        if self.verbose:
            sys.stdout.write(f"   * {group_name.lower()}\n")
        try:
            group = self.group_model_cls.objects.get(name=group_name)
        except ObjectDoesNotExist as e:
            if not create_group:
                raise ObjectDoesNotExist(f"{e} Got {group_name}")
            group = self.group_model_cls.objects.create(name=group_name)
        else:
            group.permissions.clear()
        self.add_permissions_to_group_by_codenames(group, codenames)
        self.remove_historical_group_permissions(group)

    def add_permissions_to_group_by_codenames(self, group=None, codenames=None):
        if codenames:
            permissions = self.get_permissions_qs_from_codenames(codenames)
            for permission in permissions:
                group.permissions.add(permission)

    def get_permissions_qs_from_codenames(self, codenames):
        """Returns a list of permission model instances for the given
        codenames.

        Codenames is a list or function that returns a list
        """
        permissions = []
        try:
            expanded_codenames = codenames()
        except TypeError:
            expanded_codenames = codenames
        for dotted_codename in expanded_codenames:
            try:
                app_label, codename = self.get_from_dotted_codename(dotted_codename)
            except PermissionsCodenameError as e:
                warn(str(e))
            else:
                try:
                    permissions.append(
                        self.permission_model_cls.objects.get(
                            codename=codename, content_type__app_label=app_label
                        )
                    )
                except ObjectDoesNotExist as e:
                    errmsg = f"{e}. Got codename={codename},app_label={app_label}"
                    if EDC_AUTH_CODENAMES_WARN_ONLY:
                        warn(style.ERROR(errmsg))
                    else:
                        raise ObjectDoesNotExist(errmsg)
                except MultipleObjectsReturned as e:
                    raise MultipleObjectsReturned(
                        f"{str(e)} See `{app_label}.{codename}`."
                    )
        return permissions

    def get_from_dotted_codename(self, codename=None):
        """Returns a tuple of app_label, codename.

        Validates given codename.
        """
        if not codename:
            raise PermissionsCodenameError("Invalid codename. May not be None.")
        try:
            app_label, _codename = codename.split(".")
        except ValueError as e:
            raise PermissionsCodenameError(
                f"Invalid dotted codename. {e} Got {codename}."
            )
        else:
            try:
                self.apps.get_app_config(app_label)
            except LookupError:
                raise PermissionsCodenameError(
                    f"Invalid app_label in codename. Expected format "
                    f"'<app_label>.<some_codename>'. Got {codename}."
                )
        return app_label, _codename

    def remove_pii_permissions_from_group(self, group):
        for model in self.pii_models:
            self.remove_permissions_by_model(group, model)

    @staticmethod
    def remove_historical_group_permissions(group=None, model=None):
        """Removes permissions for historical models from this
        group.

        Default removes all except `view`.
        """

        opts = dict(codename__contains="_historical")
        if model:
            opts.update(model=model)
        for permission in group.permissions.filter(**opts).exclude(
            codename__startswith="view_historical"
        ):
            group.permissions.remove(permission)

    def remove_permissions_by_model(self, group=None, model=None):
        try:
            model_cls = self.apps.get_model(model)
        except LookupError as e:
            warn(f"{e}. Got {model}")
        else:
            content_type = self.content_type_model_cls.objects.get_for_model(model_cls)
            for permission in self.permission_model_cls.objects.filter(
                content_type=content_type
            ):
                group.permissions.remove(permission)

    def create_permissions_from_tuples(self, model=None, codename_tuples=None):
        """Creates custom permissions on model "model"."""
        if codename_tuples:
            try:
                model_cls = self.apps.get_model(model)
            except LookupError as e:
                warn(f"{e}. Got {model}")
            else:
                content_type = self.content_type_model_cls.objects.get_for_model(
                    model_cls
                )
                for codename_tpl in codename_tuples:
                    app_label, codename, name = self.get_from_codename_tuple(
                        codename_tpl, model_cls._meta.app_label
                    )
                    try:
                        self.permission_model_cls.objects.get(
                            codename=codename, content_type=content_type
                        )
                    except ObjectDoesNotExist:
                        self.permission_model_cls.objects.create(
                            name=name, codename=codename, content_type=content_type
                        )
                    self.verify_codename_exists(f"{app_label}.{codename}")

    def verify_codename_exists(self, codename):
        app_label, codename = self.get_from_dotted_codename(codename)
        try:
            permission = self.permission_model_cls.objects.get(
                codename=codename, content_type__app_label=app_label
            )
        except ObjectDoesNotExist as e:
            raise CodenameDoesNotExist(f"{e} Got '{app_label}.{codename}'")
        except MultipleObjectsReturned as e:
            raise CodenameDoesNotExist(f"{e} Got '{app_label}.{codename}'")
        return permission

    @staticmethod
    def get_from_codename_tuple(codename_tpl, app_label=None):
        try:
            value, name = codename_tpl
        except ValueError as e:
            raise ValueError(f"{e} Got {codename_tpl}")
        _app_label, codename = value.split(".")
        if app_label and _app_label != app_label:
            raise PermissionsCreatorError(
                f"app_label in permission codename does not match. "
                f"Expected {app_label}. Got {_app_label}. "
                f"See {codename_tpl}.",
                code=INVALID_APP_LABEL,
            )
        return _app_label, codename, name

    def remove_permissions_by_codenames(self, group=None, codenames=None):
        """Remove the given codenames from the given group."""
        permissions = self.get_permissions_qs_from_codenames(codenames)
        for permission in permissions:
            group.permissions.remove(permission)
