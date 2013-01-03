Queries
=======
As you might have noticed, the ``query`` `API <usage>`_ method only takes a name of a query. So how are the queries defined? A Geotrack query is just a regular Python module that has an ``execute`` method and is located in a *query package*, which is just a Python package specified in configuration (more on that in :ref:`configuration`).

Having the queries defined like this enables the users to define queries they need without having to add them to Geotrack directly, and without having to implement some sort of query language (our query language in this case is just Python). It also forces them to keep all the query logic in one place and not mixed in with other code.

There are three types of queries:

The "base" query
~~~~~~~~~~~~~~~~
A sort of "default" or "base" query, which every :doc:`backend <backends>` has to support. This is then used by the concrete queries. It has to handle all the basic database stuff -- filter the entries by time, location (polygon) and unit_id.

The result of this query is a sequence (``tuple``) of mappings (``dict``) that look like this::

    {
        'unit_id': 123,
        'timestamp': datetime(2012, 5, 12, 13, 11, 5),
        'location': (49.00905, 17.18262),
        'added': datetime(2012, 5, 12, 13, 12, 35),
        'foo': 42,
        'bar': 'asdf',
    }

Where ``foo`` and ``bar`` are examples of custom fields that are being stored.

*Universal* queries
~~~~~~~~~~~~~~~~~~~
These make use of the base query doing the heavy lifting through the backend and then process these results in Python. For example, this is how we could implement a query, that would compute and average of some field we are storing::

    # in a file called average.py

    def avg(seq):
        return sum(seq) / float(len(seq))

    def execute(backend, query, field, **kwargs):
        return avg([x[field] for x in query(**kwargs)])


The query receives as the first two arguments reference to the current backend and a callable that executes the base query, followed by any keyword arguments the query might need. In the example we see the function uses the ``field`` argument and passes the rest to the base query, which is a common approach.

So with the ``average`` query defined, now if we want to call it and obtain for example the average values of field ``foo`` between the 10th and 14th of November 2012, we can call it like this::

    avg_foo = geotrack.api.query('average',
        field='foo',
        start=datetime(2012, 11, 10),
        end=datetime(2012, 11, 14),
    )

*Native* queries
~~~~~~~~~~~~~~~~
Native queries are backend-specific, meaning they only work with a certain backend and make use of some of its internal capabilities. This can be used for optimizing some queries by using features provided by the actual storage system.

These queries are expected to be named in the format: ``<query_name>_<backend_name>``. When Geotrack tries to load a query, it first tries to find a native query for the backend that is currently in use, and then falls back to the universal query.

For example, if you were unhappy with the performance of the ``average`` query from the previous example and you were using a backend based on the Django ORM, called ``mybackend``, you could create a file in your own *query package*, called ``average_mybackend.py``, that would contain::

    from django.db.models.aggregates import Avg

    def execute(backend, field, **kwargs):
        return backend.query(**kwargs).aggregate(x=Avg(field))['x']

We can see in the example, that the ``execute`` method doesn't receive the ``query`` attribute that produces the *base query* results. It instead uses the ``query`` method of the backend. The difference is, that the backend's ``query`` method returns the results in a backend-specific format, in this case a `QuerySet <https://docs.djangoproject.com/en/dev/ref/models/querysets/#queryset-api>`_, which can then be used further.

So now when you would call ``geotrack.api.query('average', ...)``, the actual computation would happen in the underlying SQL database instead of the Python program.

Note that Geotrack actually contains a :doc:`built-in Django ORM based backend <backends>`.
