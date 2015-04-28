# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name="Metrocar",
    install_requires=[
        'Django==1.5.4',
        'mock==1.0.0',
        'clint==0.3.1',
        'django-smartadmin==0.0.2',
        'flexipy',
        'django-filter==0.8',
        'pipetools==0.2.0',
        'html5lib==0.90',
        'psycopg2==2.4.1',
        'djangorestframework==2.4.4',
        'Pillow==2.3.0',
        'nose==1.1.2',
        'django-tables==0.2',
        'WebTest==1.3.3',
        'python-dateutil==2.1',
        'django-piston==0.2.2.1',
        'selenium==2.45.0', # changed from 'selenium==2.25.0'
        'South==1.0',
        'pisa==3.0.33',
        'django-webtest==1.5.2',
        'reportlab==2.5',
        'sorl-thumbnail==11.09.1',
        'django-markdown-deux==1.0.5', # Helpdesk
        'django-bootstrap-form==3.1', # Helpdesk
        'simplejson==2.3.3', # Helpdesk
        'email-reply-parser==0.3.0', # Helpdesk
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Information Technology",
        "Topic :: Security",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
    ],
    data_files=[

    ],
    packages=['metrocar', ],
    author=u"knaisl",
    author_email='vknaisl@gmail.com',
    zip_safe=True,
    include_package_data=True,
    description="Metrocar project backend",
    long_description="Student project",
    version="1.0.0",
    url="https://www.assembla.com/spaces/wagnejan_metrocar/wiki"
)
