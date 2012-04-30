==========================
Working with documentation
==========================


How to build the HTML documentation
-----------------------------------

Run::

    $ paver html

.. sidebar:: So what is this *paver* exactly?

    See :doc:`/howto/paver`.

in the root directory of the project, that is where the ``pavement.py`` file is.

You should now find the created documentation in ``docs/_build/html``.

How to clean up (delete) the generated docs
-------------------------------------------
So you don't accidentally commit them to the VCS or something.

Run::

    $ paver doc_clean


How to generate automatic API documentation for a Python package
----------------------------------------------------------------

Run::

    $ sphinx-apidoc -o outputdir packagedir

This will generate a documentation skeleton for the package with all the
docstrings extracted from the code.

The package must be importable, i. e. on the ``PYTHONPATH``.

For details and possible options see `sphinx-apidoc documentation
<http://sphinx.readthedocs.org/en/latest/invocation.html#invocation-of-sphinx-apidoc>`_