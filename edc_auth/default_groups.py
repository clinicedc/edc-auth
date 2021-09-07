from .codenames import (
    account_manager,
    administration,
    ae,
    ae_review,
    auditor,
    celery_manager,
    clinic,
    clinic_super,
    data_manager,
    data_query,
    dispensing,
    everyone,
    export,
    export_rando,
    get_rando,
    lab,
    lab_view,
    pharmacy,
    pii,
    pii_view,
    review,
    site_data_manager,
    statistician,
    tmg,
    tmg_review,
)
from .default_group_names import (
    ACCOUNT_MANAGER,
    ADMINISTRATION,
    AE,
    AE_REVIEW,
    AUDITOR,
    CELERY_MANAGER,
    CLINIC,
    CLINIC_SUPER,
    DATA_MANAGER,
    DATA_QUERY,
    DISPENSING,
    EVERYONE,
    EXPORT,
    EXPORT_RANDO,
    LAB,
    LAB_VIEW,
    PHARMACY,
    PII,
    PII_VIEW,
    RANDO,
    REVIEW,
    SITE_DATA_MANAGER,
    STATISTICIAN,
    TMG,
    TMG_REVIEW,
)

defaults = {
    AE: ae,
    AE_REVIEW: ae_review,
    ACCOUNT_MANAGER: account_manager,
    ADMINISTRATION: administration,
    AUDITOR: auditor,
    CELERY_MANAGER: celery_manager,
    CLINIC: clinic,
    CLINIC_SUPER: clinic_super,
    DATA_MANAGER: data_manager,
    DATA_QUERY: data_query,
    DISPENSING: dispensing,
    EVERYONE: everyone,
    EXPORT: export,
    EXPORT_RANDO: export_rando,
    LAB: lab,
    LAB_VIEW: lab_view,
    PHARMACY: pharmacy,
    PII: pii,
    PII_VIEW: pii_view,
    RANDO: get_rando,
    REVIEW: review,
    SITE_DATA_MANAGER: site_data_manager,
    STATISTICIAN: statistician,
    TMG: tmg,
    TMG_REVIEW: tmg_review,
}


def expanded_groups(groups=None):
    expanded = {}
    for k, v in groups.items():
        try:
            expanded.update({k: v()})
        except TypeError:
            expanded.update({k: v})
    return expanded


default_groups = expanded_groups(groups=defaults)
