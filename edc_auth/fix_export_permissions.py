from django.apps import apps as django_apps
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from edc_model import models as edc_models


def fix_export_permissions(app_label=None):
    """Add "import" and "export" to default permissions of add, change, delete, view.

    Needed for BaseUuidModel models with an initial migration created before edc==0.1.24.

    Provided for ``django-import-export`` integration
    """

    if app_label:
        app_configs = [django_apps.get_app_config(app_label)]
    else:
        app_configs = django_apps.get_app_configs()

    print(f"Adding `import` and `export` to default permissions")
    for app_config in app_configs:
        print(f"  * updating {app_config.name}")
        for model in app_config.get_models():
            if issubclass(model, (edc_models.BaseUuidModel,)):
                print(f"    - {model._meta.label_lower}")
                try:
                    content_type = ContentType.objects.get(
                        app_label=model._meta.app_label, model=model._meta.object_name
                    )
                except ObjectDoesNotExist as e:
                    raise ObjectDoesNotExist(f"{e} Got {model}.")
                for action in ["import", "export"]:
                    codename = f"{action}_{model._meta.label_lower.split('.')[1]}"
                    name = f"Can {action} {model._meta.verbose_name}"
                    opts = dict(name=name, content_type=content_type, codename=codename)
                    try:
                        Permission.objects.get(**opts)
                    except ObjectDoesNotExist:
                        Permission.objects.create(**opts)
                        print(f"       created for {model._meta.label_lower}")

    print(f"Done")
