Metrocar server project components
==================================

At the moment, the server application consists of two Django projects.


:mod:`metrocar`
---------------

The main **metrocar** project, which contains all the database models, business
logic and provides administration interface.

.. automodule:: metrocar.__init__
    :members:
    :undoc-members:


Subpackages:


.. toctree::
    :maxdepth: 1

    metrocar.api
    metrocar.car_unit_api
    metrocar.cars
    metrocar.config
    metrocar.invoices
    metrocar.reservations
    metrocar.subsidiaries
    metrocar.tariffs
    metrocar.tarification
    metrocar.tests
    metrocar.user_management
    metrocar.utils


:mod:`mfe`
---------------

The **mfe** project provides the *front-end* interface for end users (customers).


.. automodule:: mfe.__init__
    :members:
    :undoc-members:


Subpackages:


.. toctree::
    :maxdepth: 1

    mfe.active_pages
    mfe.cars
    mfe.config
    mfe.reservations
    mfe.users
    mfe.utils

