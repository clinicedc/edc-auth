|pypi| |travis| |codecov| |downloads|

edc-auth
--------

Authentication for the Edc

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
    
.. |travis| image:: https://travis-ci.org/clinicedc/edc-auth.svg?branch=develop
    :target: https://travis-ci.org/clinicedc/edc-auth
    
.. |codecov| image:: https://codecov.io/gh/clinicedc/edc-auth/branch/develop/graph/badge.svg
  :target: https://codecov.io/gh/clinicedc/edc-auth

.. |downloads| image:: https://pepy.tech/badge/edc-auth
   :target: https://pepy.tech/project/edc-auth
