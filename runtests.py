#!/usr/bin/env python
import logging
from pathlib import Path

from edc_test_utils import DefaultTestSettings, func_main

app_name = "edc_auth"
base_dir = Path(__file__).absolute().parent

project_settings = DefaultTestSettings(
    calling_file=__file__,
    SILENCED_SYSTEM_CHECKS=[
        "edc_sites.E001",
        "edc_sites.E002",
        "sites.E101",
        "edc_navbar.E002",
        "edc_navbar.E003",
    ],
    EDC_AUTH_CODENAMES_WARN_ONLY=True,
    EDC_AUTH_SKIP_SITE_AUTHS=True,
    EDC_AUTH_SKIP_AUTH_UPDATER=True,
    BASE_DIR=base_dir,
    APP_NAME=app_name,
    SUBJECT_VISIT_MODEL="edc_visit_tracking.subjectvisit",
    add_dashboard_middleware=True,
    add_lab_dashboard_middleware=True,
    use_test_urls=True,
).settings


def main():
    func_main(project_settings, f"{app_name}.tests")


if __name__ == "__main__":
    logging.basicConfig()
    main()
