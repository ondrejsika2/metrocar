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

.. note::

    If you don't plan on working on geo-related functionality within the project, you can install any database you want (provided it is `supported by Django <https://docs.djangoproject.com/en/dev/topics/install/#database-installation>`_).

    Just put ``GEO_ENABLED = False`` in your ``settings/local.py``.

    Otherwise, you have to get a database that `works with GeoDjango <https://docs.djangoproject.com/en/dev/ref/contrib/gis/tutorial/#setting-up>`_


Your best bet is PostgreSQL. A short excerpt from `the complete tutorial <https://docs.djangoproject.com/en/dev/ref/contrib/gis/tutorial/#setting-up>`_ that should work in Debian / Ubuntu:

First install PostgreSQL::

    $ sudo apt-get install postgresql-9.1-postgis postgresql-server-dev-9.1

After that, you need to log in as user postgres::

    $ sudo su postgres

Create database user metrocar::

    $ createuser -P metrocar

You will be asked for a password (I recommend to use password: metrocar). After
that, answer no to every question except if the user can create database (it's
needed for creating a testing database when running tests).

After that you have to create template for postgres. Download script `create_template_postgis-debian.sh <https://docs.djangoproject.com/en/dev/_downloads/create_template_postgis-debian1.sh>`_ which is for debian/ubuntu.

Then run the script as user postgres::

    $ sh create_template_postgis-debian.sh

After that you need to create database. Run psql and enter::

    CREATE DATABASE metrocar OWNER metrocar TEMPLATE template_postgis ENCODING 'UTF8';

Then as user root, edit file ``/etc/postgresql/9.1/main/pg_hba.conf`` and comment
out the line ``local all all peer`` and insert new line ``local all all trust``

As user root, restart postgres server::

    $ sudo /etc/init.d/postgresql restart

5. Update your development settings
===================================

Create a file named ``metrocar/settings/local.py`` and fill-in your development
settings. See ``metrocar/settings/local_example.py`` for inspiration.


6. Run the tests
================

You should now :ref:`run the test suite <running-tests>` to make sure everything
works.
