# encoding: utf-8
"""
A management command to populate the database with testing data.

Attempts to load testing data from all apps in ``INSTALLED_APPS`` if they provide
it.

Run with ``-v 2`` or ``-v 3`` for debugging.


An app can provide testing data the following way:
--------------------------------------------------

* It contains a module (or possibly a package) called ``testing_data`` that
  defines a ``create()`` method

* This method doesn't take any arguments and when called, should create
  testing data for the app and return them in the following format::

    {
        'model_name': [instance, instance, ...],
        'other_model_name': [...],
        # ...
    }

  For example, a blogging app's ``testing_data.create`` could return
  something like this::

    {
        'blog_posts': [test_post1, test_post2, ...],
        'authors': [test_author],
    }

* Usually it's convenient if the ``create`` method is **idempotent** -- doesn't
  create more data when it's called again with the database already
  populated.

  This can be easily achieved by using the ``MyModel.objects.get_or_create``
  method.

* These ``create`` scripts can also be conveniently used in tests.

"""

import traceback
from clint.textui import colored

from django.conf import settings
from django.core.management.base import NoArgsCommand


def report_result(data):
    """
    Prints a report on created testing data for an app.
    """
    if isinstance(data, dict):
        print ', '.join('%s %s' % (colored.green(len(value)), key)
            for key, value in data.iteritems())
    elif isinstance(data, (tuple, list)):
        print colored.green(len(data)) + ' items'
    elif data is None:
        print colored.red('X')
    else:
        print colored.yellow('?')


class Command(NoArgsCommand):
    help = 'Populates db with testing data from apps.'

    def handle_noargs(self, **options):
        verbosity = int(options.get('verbosity'))
        for app in settings.INSTALLED_APPS:
            mod = app + '.testing_data'
            try:
                testing_data = __import__(mod, {}, {}, ['create'])
            except ImportError, e:
                if verbosity > 1:
                    print "Couldn't import %s: %s" % (mod, e)
                if verbosity > 2:
                    traceback.print_exc()
                continue
            if not hasattr(testing_data, 'create'):
                if verbosity > 1:
                    print "%s doesn't contain a create function" % mod
                continue
            print 'Loading testing data for %s...' % app,
            report_result(testing_data.create())
