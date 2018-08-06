|pypi| |travis| |coverage|

edc-auth
--------

Authentication for the Edc



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
    
.. |coverage| image:: https://coveralls.io/repos/github/clinicedc/edc-auth/badge.svg?branch=develop
    :target: https://coveralls.io/github/clinicedc/edc-auth?branch=develop

