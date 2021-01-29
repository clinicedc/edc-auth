|pypi| |actions| |codecov| |downloads|

edc-auth
--------

Authentication and permissions for the Edc

Default Groups
++++++++++++++


The default groups are required for the normal operation of an EDC deployment. The default groups are:

* ``ACCOUNT_MANAGER``: members may add/change and delete user accounts
* ``ADMINISTRATION``: members may view the Administration page
* ``AUDITOR``: members may view all forms but have no add/change permissions.
* ``CLINIC``: members may add/edit/delete all CRFs, Requisitions, Actions and other required clinic trial data entry forms. They may also view the Requisition page of the Lab section;
* ``EVERYONE``: members may access the EDC;
* ``LAB``: members may perform all functions in the Lab section (Edit requisitions, receive, process, pack, manage manifests, etc);
* ``PHARMACY``:
* ``PII``: members may view all personally identifiable data and edit forms that manage such data (Screening, Consents, Patient registration);
* ``PII_VIEW``: members may view personally identifiable data but have no add/edit permissions for any of the forms that store such data.

Permissions
+++++++++++

Permissions use Django's permission framework,  therefore, all permissions are linked to some model.

Permissions don't always naturally link to a model. In such cases, a dummy model is created. For example, with Navigation bars from `edc_navbar`. Permissions to follow an item on a navigation bar are associated with model `edc_navbar.Navbar`. A similar approach is used for `listboard` permissions using `edc_dashboard.Dashboard`.


Importing users
+++++++++++++++

You create user accounts by importing a specially formatted CSV file. Once an account is created a "Welcome" email may be sent.

Import users from a CSV file with columns:

.. code-block:: bash

	username
	first_name
	last_name
    job_title
    email
    alternate_email
    mobile
    sites: a comma-separated list of sites
    groups: a comma-separated list of groups


Then import the users from your application commandline

.. code-block:: bash

	python manage.py import_users --csvfile=/Users/erikvw/meta_users.csv --notify-to-test-email=ew2789@gmail --resource-name=meta.clinicedc.org --resend-as-new

Legacy notes
++++++++++++

**Important:** If you are upgrading from edc_base.auth:

The ``userprofile`` table is now in ``edc_auth``. ``edc_auth`` has one migration for this table.
Copy the same table from ``edc_base`` and fake the ``edc_auth`` migration.

.. code-block:: sql

	CREATE TABLE edc_auth_userprofile LIKE edc_base_userprofile;

	INSERT edc_auth_userprofile SELECT * FROM edc_base_userprofile;


.. code-block:: bash

	python manage.py migrate edc_auth --fake

You can now run the ``edc_base`` migration safely.

.. |pypi| image:: https://img.shields.io/pypi/v/edc-auth.svg
    :target: https://pypi.python.org/pypi/edc-auth

.. |actions| image:: https://github.com/clinicedc/edc-auth/workflows/build/badge.svg?branch=develop
  :target: https://github.com/clinicedc/edc-auth/?query=workflow:build

.. |codecov| image:: https://codecov.io/gh/clinicedc/edc-auth/branch/develop/graph/badge.svg
  :target: https://codecov.io/gh/clinicedc/edc-auth

.. |downloads| image:: https://pepy.tech/badge/edc-auth
   :target: https://pepy.tech/project/edc-auth
