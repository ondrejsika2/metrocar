About Metrocar
==============

Metrocar is a long running project on CTU's `Faculty of Electrical Engineering
(a.k.a. FEL)`_ that attempts to create a more or less universal
:doc:`carsharing <carsharing>`-management solution, which could be deployed by
a carsharing organization to handle common tasks such as reservations
or billing.


The server / web application
----------------------------
The primary component of this system is the server-side application which
handles the database and provides interfaces for users, administrators and
other systems.


Car unit
--------
There are also at least two sub-projects aimed at creating a so called
*car-unit* -- a device (and software) to be installed in the rental cars
to monitor their movement and status and also to enable a convenient way to
access them -- using a Bluetooth-enabled cellphone or an RFID card.

The system should, however, be able to function even without the units.

.. todo::

    **TODO** Links to the projects.


.. seealso::

    :doc:`/components/metrocar.car_unit_api`


Mobile application(s)
---------------------
The Bluetooth-unlockable car unit will also require a counterpart that will
be installable on the users' mobile devices.

There are also plans for a mobile application for managing reservations,
though that would probably best be done by a responsive web design of the
regular front-end.



.. _Faculty of Electrical Engineering (a.k.a. FEL): http://www.fel.cvut.cz/
