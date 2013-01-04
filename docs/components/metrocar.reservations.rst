metrocar.reservations
============================

This application deals with reservations.

Reservations are related to a specific :class:`~metrocar.cars.models.Car`. When completed, they can consist of several :class:`~metrocar.cars.models.Journey` s. The price to be paid for a completed reservation is computed from the Journeys' data using a :class:`~metrocar.tarification.models.Pricelist` and added to the user's :class:`~metrocar.user_management.models.Account` in the form of :class:`~metrocar.reservations.models.ReservationBill`.




:mod:`models`
--------------------

.. automodule:: metrocar.reservations.models
    :members:
    :undoc-members:
    :show-inheritance:

:mod:`managers`
----------------------

.. automodule:: metrocar.reservations.managers
    :members:
    :undoc-members:
    :show-inheritance:

:mod:`forms`
-------------------

.. automodule:: metrocar.reservations.forms
    :members:
    :undoc-members:
    :show-inheritance:

Subpackages
-----------

.. toctree::

    metrocar.reservations.api
    metrocar.reservations.management
    metrocar.reservations.plugins

