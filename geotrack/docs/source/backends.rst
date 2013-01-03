Backends
========
The backend is where most of the work gets done. It's basically a wrapper for a storage / database system, much like Django's database backend. But unlike Django's DB backend, this one only has to support quite narrow spectrum of functionality and therefore is easier to implement for a wide variety of storage systems (whereas implementing Django's ORM backend for anything else than an SQL database would be quite the adventure).

A valid Geotrack backend has to be a python module / package that provides the following methods:

* ``store(unit_id, timestamp, location, added, **kwargs)``

  basically identical to the `public API one <usage>`_, except it has an extra argument ``added``, used to store when the particular *entry* arrived in the system, which can be useful for debugging or audit.

* ``query(start=None, end=None, in_polygon=None, units=None)``

  This should implement the *base* query and optionally return a result in some
  intermediate format, that can be further used by *native* queries.

* ``transform(query_result)``

  This should transform the intermediate result from ``query`` to the "universal" format -- which is what :doc:`universal queries <queries>` get to work with and what will in some cases be returned to the client, and therefore should only consist of *values*.

* ``query_last_position(start=None, end=None, in_polygon=None, units=None)``

  Because the *last known position* query is so important and needs to be fast, and handling it through the regular query would mean significant overhead for basically any type of backend (filtering, sorting and selecting the last value for each unit), the backends are expected to provide this method that will provide an efficient way of getting the last positions.

Built-in backends
-----------------

GeoDjango
~~~~~~~~~
Path: ``geotrack.backends.geodjango``

This backend uses `GeoDjango <https://docs.djangoproject.com/en/dev/ref/contrib/gis/>`_ models for storing entries.

To use this backend, the project you use Geotrack with has to have a GeoDjango compatible database backend.

Also (unless you want to only store time and location), to specify what kind of fields you want to store for each entry, you have to supply a model which will be used for storage. It's probably best to inherit it from ``geotrack.backends.geodjango.models.LogEntryBase``.

For example,

in your_app/models.py::

	from geotrack.backends.geodjango.models import LogEntryBase

	class MyLogEntry(LogEntryBase):
		my_extra_field = models.CharField()
		another_field = models.FloatField()

and in settings::

	GEOTRACK = {
	    'BACKEND': 'geotrack.backends.geodjango',
	    'MODEL': 'your_app.MyLogEntry',

	    # optionally, you can also specify the SRID to use
	    # see GeoDjango docs for more information
	    'SRID': 4326,
	}


Dummy backend
~~~~~~~~~~~~~
Path: ``geotrack.backends.dummy``

A dummy backend that returns an empty result for everything.
