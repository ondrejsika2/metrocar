#!/usr/bin/env python

'''
simple shortcut for running nosetests via python
replacement for *.bat or *.sh wrappers
'''

import os
from os.path import join, pardir, abspath, dirname, split

import nose


# django settings module
DJANGO_SETTINGS_MODULE = '%s.%s' % (split(abspath(dirname(__file__)))[1], 'settings.local')
os.environ['DJANGO_SETTINGS_MODULE'] = DJANGO_SETTINGS_MODULE

nose.run_exit(
    defaultTest=dirname(__file__),
)
