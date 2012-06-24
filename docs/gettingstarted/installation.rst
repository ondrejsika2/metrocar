============
Installation
============

.. note:: *Word of advice*

    If it is at all possible for you, it is highly recommended to develop
    the project in a Unix-based OS, as that's what most of the devs use
    and you are likely to run into a lot less problems there.


.. highlight:: bash


1. Get the code
===============

.. sidebar:: Why Git?

    .. include:: why-git.rst

The code is in Git.

::

    $ git clone git@git.assembla.com:wagnejan_metrocar.git metrocar

``git@git.assembla.com:wagnejan_metrocar.git`` is the main repository. Ask the
:ref:`project-maintainer` to grant you access. In the meantime, you can get the
code via the Public clone URL:

``git://git.assembla.com/wagnejan_metrocar.git``


.. seealso::
    Are you new to Git? See: :doc:`/howto/git`


2. Create a virtualenv (optional, but highly recommended)
=========================================================

Virtualenv_ is a tool for creating isolated python environments. It allows you
to install python packages without cluttering your OS's main python
installation.

First you need to install_ it on your system, if you don't have it already.

Then you can create a virtual environment for the project like so::

    $ virtualenv metrocar-env --no-site-packages

Where ``metrocar-env`` is a directory where the virtualenv will be created. It
can be anywhere you like (but don't create it inside the repository, so you
don't later commit it by accident) and you can use the environment even outside
this directory.

To use it, you have to activate it::

    $ . metrocar-env/bin/activate

To deactivate it later, you simply run::

    $ deactivate

(In any directory)

.. note::

    This differs a bit when you are on Windows, please refer to `virtualenv
    documentation`_.



.. _Virtualenv: http://pypi.python.org/pypi/virtualenv
.. _install: http://pypi.python.org/pypi/virtualenv
.. _virtualenv documentation: http://pypi.python.org/pypi/virtualenv


3. Install the python packages
==============================

Go to the repository you cloned in first step (with the virtualenv activated, if
you have it)::

    $ cd metrocar

Install the project's packages::

    $ python setup.py develop

Install the dependencies::

    $ paver install_dependencies


4. Setup a database
===================

At the moment the project is dependent on a PostgreSQL with a geo tepmlate which
is kind of a hassle to set up. I hope to remove this dependency so I  won't need
to write about how to get it running. If you need to install the project before
then, see geo-django documentation or try your luck with the legacy
documentation:

* `<http://www.assembla.com/spaces/wagnejan_metrocar/wiki/SI2_-_Home>`_
* `<http://www.assembla.com/spaces/wagnejan_metrocar/documents>`_
* `<http://www.assembla.com/spaces/metrocar/wiki/Zprovozneni_Webservice_Ubuntu10_04_PostgreSQL8_4>`_


5. Update you development settings
==================================

Put your development database login information in config/settings_local.py

TODO: settings refactoring pending.


6. Run the tests
================

You should now :ref:`run the test suite <running-tests>` to make sure everything
works.
