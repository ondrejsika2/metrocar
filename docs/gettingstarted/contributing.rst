Contribution guidelines
=======================

.. note:: Please read this before adding any new code to the project.

    (Unless you're a Python/Django veteran)

Yes, it takes some time to study these things, but it's well worth it.
It will be far more valuable if you add just one small, but well coded
feature with documentation and tests, as opposed to hacking together a bunch
of stuff that might work now, but people are going to have to spend a
lot of hours later figuring out what the hell it does, how is it supposed to
work and why is it broken.

Not only is this better for the project, but also for *you* -- if you're doing
this to learn something useful, that is.

.. _contributing-coding-style:

Coding style
------------

Basically, just follow the `Django coding style <https://docs.djangoproject.com/en/dev/internals/contributing/writing-code/coding-style/>`_.

The `PEP8`_ official Style Guide for Python Code is quite important and useful.
It may seem strange if you come from some other languages, but it is
not merely *some convention* it's actually part of the language specification.

You don't necessarily have to read it (though you should if you are serious
about Python), you can just use the ``pep8`` command line utility or, even
better, get a plugin for you editor that will highlight incorrect formatting
for you.

.. _PEP8: http://www.python.org/dev/peps/pep-0008/


.. _contributing-documentation:

Documentation
-------------

In a project of this size, with multiple people working on it for relatively
short intervals, **documentation is kinda important**.

.. image:: /_static/docs-motivator.jpeg

* **If you add something** to the project, like a new Django-app, for example,
  **write at least one sentence about what it does**. This can be very helpful
  for new people coming to the project.

* **If you change something**, don't forget to **update the documentation**.

  * At the very least, delete what no longer applies.

* By not following these rules, you will most likely cause a massive headache
  to people who'll be picking up the project after you.


`PyCon 2011: Writing great documentation <http://blip.tv/pycon-us-videos-2009-2010-2011/pycon-2011-writing-great-documentation-4899042>`_


.. _contributing-testing:

Tests
-----

.. sidebar:: Testable code

    .. include:: testable-code.rst


Tests are pretty important too. Without them, you can never be sure if your
new code didn't break some of the old one. Unless you want to test everything
manually every time.

* Be sure to run the tests and check none of them are failing before you
  commit (push) your code to repository.

* If you make a clean check-out and the tests don't pass on that, you can:

    * fix it
    * complain to the guy who broke it, or if you can't find out who that is,
      to the :ref:`project-maintainer`

* If you add new functionality it'd be nice if you also added at least some
  basic tests for it, so that no one will unintentionally break it in the
  future

.. seealso::
    :doc:`/howto/tests`

Testing data
~~~~~~~~~~~~

.. include:: testing-data.rst

For instructions on how to expose testing data for an app and bootstrap the
database with testing data from all apps, see the
:mod:`~metrocar.utils.management.commands.load_dummy_data` command.

For an example, see ``metrocar.cars.testing_data.py``.


Some resources on writing tests in Django
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* http://readthedocs.org/docs/pycon-2012-notes/en/latest/testing_and_django.html
* http://toastdriven.com/blog/2011/apr/10/guide-to-testing-in-django/
* http://blip.tv/djangocon-europe-2010/honza-kr%C3%A1l-testing-django-applications-3696434
* http://www.tdd-django-tutorial.com
