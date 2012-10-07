==========================
Database schema migrations
==========================

Django's built-in ``syncdb`` command isn't very helpful when it comes to
changing already existing models (which happens to be all the time). And doing
the changes by hand and distributing them to other developers by email isn't a
very sustainable solution.

Therefore we make use of a third-party solution: South_, which has now became
the de-facto standard for Django schema migrations.

You can find all the info in the `documentation`_, but mostly you will just need
to do the following:


Apply new migrations
--------------------
When new migrations arrive in the VCS, you can apply them like this::

    $ python manage.py migrate


Create an automatic migration for an app
----------------------------------------
When you make some changes, let South figure out what needs to be done
automatically, by comparing current source to a frozen db schema::

    $ python manage.py schemamigration app --auto

This works on a per-app basis, so replace "app" with a real app you want to
migrate.

Also this doesn't work at all times, so when it doesn't, follow the on screen
instructions and/or consult South's documentation_.


Create a data migration
-----------------------
You just want to move some data about, fair enough::

    $ python manage.py datamigration app

Now you have to fill in the changes in the generated migration file.


.. _South: http://south.readthedocs.org/en/latest/
.. _documentation: http://south.readthedocs.org/en/latest/


