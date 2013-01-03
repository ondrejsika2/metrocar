Installation
============

1. Run::

	python setup.py install

2. Update your Django project's settings::

	GEOTRACK = {
	    # specify path to a backend
	    'BACKEND': 'some.geo.backend',

	    # optionally specify a list of packages containing query definitions
	    'QUERY_PACKAGES': [
	    	'your_app.geo_queries',
	    ]
	}

3. See your selected backend's documentation for any additional settings or installation requirements.
