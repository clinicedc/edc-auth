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
