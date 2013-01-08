.. Metrocar documentation master file, created by
   sphinx-quickstart on Sat Mar 24 19:09:20 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

==================================
Welcome to Metrocar documentation!
==================================

This documentation covers primarily the server-side component, which is written
in Python_ and on top of the Django_ framework. :doc:`Read more about
this documentation <overview/about>`.


.. _Python: http://www.python.org/
.. _Django: https://www.djangoproject.com/


Overview
========
The big picture

* :doc:`overview/carsharing`

* :doc:`overview/metrocar`

* :doc:`overview/about`

* :doc:`overview/people`



Getting started
===============

* :doc:`gettingstarted/prerequisites` -- what you should know (take a look at) before you start,
  Python/Django tutorials, etc.

* :doc:`gettingstarted/installation` -- how to get the project up and running.

* :doc:`gettingstarted/contributing` -- some hints to follow to not make a (*bigger than it already is*) mess of this project.

  * :ref:`contributing-coding-style`
  * :ref:`contributing-documentation`
  * :ref:`Testing <contributing-testing>`


How to...
=========

* :doc:`...work with Git <howto/git>`
* :doc:`...run the test suite <howto/tests>`
* :doc:`...work with the documentation <howto/documentation>`
* :doc:`...create and apply database schema migrations <howto/south>`
* :doc:`...project task automation / build system <howto/paver>`
* :doc:`...deploy to the production server <howto/deployment>`
* :doc:`...work with geographic data within Metrocar <howto/geo>`
* :doc:`...write JavaScript <howto/js>`
* :doc:`...write better code <howto/code>`


System components' documentation
================================

.. toctree::
    :maxdepth: 3

    components/index


Indices and tables
==================

* :doc:`Detailed table of contents <contents>`
* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


Full contents
=============

.. toctree::
    :maxdepth: 1

    index
    about

.. toctree::
    :maxdepth: 3

    overview/index
    gettingstarted/index
    howto/index
    components/index
