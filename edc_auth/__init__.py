from .get_default_codenames_by_group import get_default_codenames_by_group
from .group_names import (
    ACCOUNT_MANAGER,
    ADMINISTRATION,
    AE,
    AE_REVIEW,
    AUDITOR,
    CELERY_MANAGER,
    CLINIC,
    DATA_MANAGER,
    DISPENSING,
    SITE_DATA_MANAGER,
    DATA_QUERY,
    EVERYONE,
    EXPORT,
    LAB,
    LAB_VIEW,
    PHARMACY,
    PII,
    PII_VIEW,
    RANDO,
    REVIEW,
    SCREENING,
    TMG,
    UNBLINDING_REQUESTORS,
    UNBLINDING_REVIEWERS,
)

codenames_by_group = {k: v for k, v in get_default_codenames_by_group().items()}


def slugify_user(user):
    return f"{user.first_name}-{user.last_name}-{user.username}-{user.email}"
