#!/usr/bin/env python
import logging
from os.path import abspath, dirname

from edc_constants.constants import IGNORE
from edc_test_utils import DefaultTestSettings, func_main

app_name = "edc_auth"
base_dir = dirname(abspath(__file__))

project_settings = DefaultTestSettings(
    calling_file=__file__,
    EDC_NAVBAR_VERIFY_ON_LOAD=IGNORE,
    EDC_AUTH_CODENAMES_WARN_ONLY=True,
    EDC_AUTH_SKIP_SITE_AUTHS=True,
    EDC_AUTH_SKIP_AUTH_UPDATER=True,
    BASE_DIR=base_dir,
    APP_NAME=app_name,
    add_dashboard_middleware=True,
    add_lab_dashboard_middleware=True,
    use_test_urls=True,
).settings


def main():
    func_main(app_name, project_settings)


if __name__ == "__main__":
    logging.basicConfig()
    main()
