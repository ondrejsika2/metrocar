metrocar.settings
=================

The project's settings are the form of a package.


:mod:`base` Module
------------------

The ``base`` module contains the project's production settings without any credentials that shouldn't be present in the VCS -- as that's publicly available on the Internet.


:mod:`local` Module
-------------------

The ``local`` module should contain settings that override the ``base`` settings for the specific environment where the project is installed. These shouldn't be in the VCS at all, each developer should create their own version.

This module can also hold the credentials needed for the version deployed on production.


:mod:`local_example` Module
---------------------------

This module contains an example of what could be placed in the ``local`` settings for development.

It can be even imported in the ``local`` module for convenience.
