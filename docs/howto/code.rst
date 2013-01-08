Some tips on how to write better code
=====================================

This section contains some resources with general advice on programming and software design.

Talks / articles
----------------

* `Simple made Easy <http://www.infoq.com/presentations/Simple-Made-Easy>`_

  Our greatest enemy is (incidental) complexity. Watch this talk by Rich Hickey to see what tools you can use to avoid it. And also to understand it might not be *easy*. There's also a bit different, `shorter version <http://www.youtube.com/watch?v=rI8tNMsozo0>`_.


* `Value of values <http://www.infoq.com/presentations/Value-Values>`_

  This talk, again by Rich Hickey, shows us what's wrong with most of todays technology for building information systems (which includes Django as well) -- which is based on PLOP. Unfortunately there doesn't appear to be many actually useful alternatives, so we're stuck with it for now. But we can still leverage the power of values.


* `John Carmack explains the practical benefits of functional programming <http://www.altdevblogaday.com/2012/04/26/functional-programming-in-c/>`_

  He even uses it in C++, so we can definitely take advantage of it in Python where it's much easier.


Tools
-----

Code analysis
"""""""""""""
You should definitely take a look at `pylint <http://www.pylint.org/>`_ and `pyflakes <https://launchpad.net/pyflakes>`_. `Find out <http://google.com>`_ how to integrate them in your editor and you'll be notified of syntax errors, undefined variables, unused imports, improper formatting and more in real-time. They work great in SublimeText (via SublimeCodeIntel), Eclipse, and probably also others but I haven't tried that.

IPython
"""""""
Another invaluable tool is `IPython <http://ipython.org/>`_ (``pip install ipython``) which is a (much) better Python interactive shell with tab-auto-completion and many other useful features. Once you install it, Django's ``manage.py shell`` will automatically use it. You can also embed it inside your program for interactive debugging -- just insert the following line into your code::

	import IPython; IPython.embed()
