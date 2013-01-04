Dealing with geographic data
============================

Data formats
------------

Point
~~~~~
The canonic format for a location, or point, is a two-item sequence, where the first item is longitude and the second one latitude. Which can be also referenced X and Y coordinates. The values are in degrees as floating point numbers and use the WGS84 reference system (the most common one).

Example::

	location = (14.41861, 50.07604)

Polygon
~~~~~~~
A sequence of *points* that represents a polygon. The last item should be the same as the first, for easy convertibility to `WKT <http://en.wikipedia.org/wiki/Well-known_text>`_


Geotrack
--------
`Geotrack <http://autonapul.cz/docs/geotrack/>`_ is a primary geographic storage used for this project. See its `documentation <http://autonapul.cz/docs/geotrack/>`_.


There are various utilities for working with geo data in the :mod:`metrocar.utils.geo` package.
