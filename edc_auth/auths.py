from .default_groups import default_groups
from .default_pii_models import default_pii_models
from .default_roles import default_roles
from .site_auths import site_auths

site_auths.register(
    groups=default_groups,
    roles=default_roles,
    pii_models=default_pii_models,
)
