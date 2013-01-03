Usage
=====

With Geotrack installed, you can make use of it using it's public API, accessible as ``geotrack.api``.

Geotrack operates on *log entries* -- information about a specific time (``timestamp``) and place (``location``) of a specific *unit*, along with any other data you wish to store. A *unit* is a device that you will be tracking. It can be installed in a car or any other moving thing you wish to track.

The *log entries* are associated with the *units* using an externally provided unique identifier, which will be (in text and code) referred to as ``unit_id``. Geotrack doesn't care about any properties of the units other than this identifier; they are expected to be managed elsewhere.


Provided methods
~~~~~~~~~~~~~~~~
The API provides two main methods:

- ``geotrack.api.store(unit_id, timestamp, location, **kwargs)``

  The ``store`` method creates a *log entry* in the system with the given ``timestamp``, ``location`` and any other values ``**kwargs`` may hold, associated with a unit identified by ``unit_id``.

- ``geotrack.api.query(query_name, **kwargs)``

  The ``query`` method executes a query defined for ``query_name`` (see :ref:`query-mechanism` for details) with any given keyword arguments (mapping) from ``**kwargs`` and returns the results. This is always a blocking call and possible background processing of longer-running queries should be handled by the caller (or some special middle-ware).

There is also ``geotrack.api.flush()`` to delete all stored content -- useful for testing.

.. seealso:: :doc:`How queries work<queries>`


Access to the API
~~~~~~~~~~~~~~~~~
The Geotrack package itself only provides access to the API via Python. But the fact the the API only uses *values* and that `values are essentially language-agnostic <http://www.infoq.com/presentations/Value-Values>`_ makes it possible to easily create an adapter for any kind of language or protocol, most notably, HTTP.

One could create a simple "wrapper" Django project, that would just contain the Geotrack app and an adapter to serialize and de-serialize data to JSON and expose the API methods through HTTP, and then Geotrack could be used from any language. It could also be accessed across the network if need be, which could be useful in some scenarios, for example to deploy it on a dedicated machine to deal with higher loads.
