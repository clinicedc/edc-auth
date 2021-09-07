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
from edc_randomization.site_randomizers import site_randomizers

from ..codename_tuples import dashboard_tuples, get_rando_tuples, navbar_tuples
from ..default_group_names import PII, PII_VIEW


class PermissionsCodenameError(Exception):
    pass


class PermissionsCreatorError(ValidationError):
    pass


class CodenameDoesNotExist(Exception):
    pass


INVALID_APP_LABEL = "invalid_app_label"
EDC_AUTH_CODENAMES_WARN_ONLY = getattr(settings, "EDC_AUTH_CODENAMES_WARN_ONLY", False)
# site_randomizers.autodiscover()


class GroupUpdater:
    def __init__(
        self,
        groups: Optional[dict] = None,
        apps=None,
        verbose=None,
        extra_pii_models=None,
        create_codename_tuples=None,
        **kwargs,
    ):
        self.apps = apps or django_apps
        self.groups = groups
        self.group_names = list(self.groups.keys())
        self.verbose = verbose
        self.extra_pii_models = extra_pii_models or []
        self.create_codename_tuples = create_codename_tuples
        self.group_model_cls = self.apps.get_model("auth.group")
        self.permission_model_cls = self.apps.get_model("auth.permission")
        self.content_type_model_cls = self.apps.get_model("contenttypes.contenttype")
        self.dashboard_tuples = dashboard_tuples
        self.navbar_tuples = navbar_tuples
        self.rando_tuples = get_rando_tuples()

    def update_groups(self):
        for group_name, codenames in self.groups.items():
            self.update_group(group_name, codenames, create_group=True)
        self.update_rando_group_permissions()
        self.update_other_special_group_permissions()
        self.remove_permissions_to_dummy_models()
        self.make_randomizationlist_view_only()
        for group in self.group_model_cls.objects.exclude(name__in=[PII, PII_VIEW]):
            self.remove_pii_permissions_from_group(group)
        self.group_model_cls.objects.exclude(name__in=self.group_names).delete()

    def update_rando_group_permissions(self):
        """Update group permissions for each registered randomizer class."""
        for randomizer_cls in site_randomizers._registry.values():
            if self.verbose:
                sys.stdout.write(
                    "  creating permissions for registered randomizer_cls "
                    f"`{randomizer_cls.name}` model "
                    f"`{randomizer_cls.model_cls()._meta.label_lower}`\n"
                )
            rando_tuples = [
                (k, v)
                for k, v in self.rando_tuples
                if k.startswith(
                    randomizer_cls.model_cls()._meta.label_lower.split(".")[0]
                )
            ]
            self.create_permissions_from_tuples(
                randomizer_cls.model_cls()._meta.label_lower,
                rando_tuples,
            )

    def update_other_special_group_permissions(self):
        self.create_permissions_from_tuples(
            "edc_dashboard.dashboard", self.dashboard_tuples
        )
        self.create_permissions_from_tuples("edc_navbar.navbar", self.navbar_tuples)
        for model, codename_tuples in (self.create_codename_tuples or {}).items():
            self.create_permissions_from_tuples(model, codename_tuples)
        self.create_permissions_from_tuples("edc_navbar.navbar", self.navbar_tuples)

    def update_group(self, group_name, codenames, create_group=None):
        if self.verbose:
            sys.stdout.write(f"  * {group_name.lower()}\n")
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
        default_pii_models = [
            settings.SUBJECT_CONSENT_MODEL,
            "edc_locator.subjectlocator",
            "edc_registration.registeredsubject",
        ]
        default_pii_models.extend(self.extra_pii_models)
        for model in default_pii_models:
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

    def remove_permissions_to_dummy_models(self):
        for group in self.group_model_cls.objects.all():
            self.remove_permissions_by_codenames(
                group=group,
                codenames=[
                    "edc_dashboard.add_dashboard",
                    "edc_dashboard.change_dashboard",
                    "edc_dashboard.delete_dashboard",
                    "edc_dashboard.view_dashboard",
                    "edc_navbar.add_navbar",
                    "edc_navbar.change_navbar",
                    "edc_navbar.delete_navbar",
                    "edc_navbar.view_navbar",
                ],
            )

    def remove_permissions_by_codenames(self, group=None, codenames=None):
        """Remove the given codenames from the given group."""
        permissions = self.get_permissions_qs_from_codenames(codenames)
        for permission in permissions:
            group.permissions.remove(permission)

    def make_randomizationlist_view_only(self):
        for randomizer_cls in site_randomizers._registry.values():
            app_label, model = randomizer_cls.model_cls(
                apps=self.apps
            )._meta.label_lower.split(".")
            permissions = self.permission_model_cls.objects.filter(
                content_type__app_label=app_label, content_type__model=model
            ).exclude(codename=f"view_{model}")
            codenames = [f"{app_label}.{o.codename}" for o in permissions]
            codenames.extend(
                [
                    f"{app_label}.add_{model}",
                    f"{app_label}.change_{model}",
                    f"{app_label}.delete_{model}",
                ]
            )
            codenames = list(set(codenames))
            for group in self.group_model_cls.objects.all():
                self.remove_permissions_by_codenames(
                    group=group,
                    codenames=codenames,
                )
