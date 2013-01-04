metrocar.tarification
=====================

This application handles the regular pricing of :mod:`~metrocar.reservations`.

There is a separate :class:`~metrocar.tarification.models.Pricelist` for each :class:`~metrocar.cars.models.CarModel`. The price list then consists of one or several :class:`~metrocar.tarification.models.PricelistDay` s which in turn consist of one or more :class:`~metrocar.tarification.models.PricelistDayTime`.


:mod:`models`
--------------------

.. automodule:: metrocar.tarification.models
    :members:
    :undoc-members:
    :show-inheritance:

:mod:`managers`
----------------------

.. automodule:: metrocar.tarification.managers
    :members:
    :undoc-members:
    :show-inheritance:



Subpackages
-----------

.. toctree::

    metrocar.tarification.api

