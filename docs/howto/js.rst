Guidelines for writing manageable JavaScript
============================================

CoffeeScript
------------
First of all, it is strongly recommended to write all JavaScript in `CoffeeScript <http://jashkenas.github.com/coffee-script/>`_. It's just *so* much better. If you don't know it and you are planning on writing any JavaScript, you should go `check it out <http://jashkenas.github.com/coffee-script/>`_.

Metrocar JavaScript guidelines
------------------------------

Where to put it?
~~~~~~~~~~~~~~~~
Any JavaScript code belonging to an application should be in that application's ``static/js`` directory (in the same way templates are, so something like: ``metrocar/some_app/static/js/some_app/...``). Any commonly useful utilities and libraries should reside in the project's ``static/js`` directory.

Modules
~~~~~~~
Use `require.js <http://www.requirejs.org/>`_ for creating and importing modules. A generic configuration which mostly handles ``shim`` definitions of commonly used libraries is in ``metrocar/static/js/require-config``.

Frameworks
~~~~~~~~~~
The recommended front-end framework is `Backbone <http://backbonejs.org/>`_.

Testing
~~~~~~~
The testing framework is `Mocha <http://visionmedia.github.com/mocha/>`_ + `Chai <http://chaijs.com/>`_.

At the moment, the tests are conducted via browser, see the ``metrocar/tests`` app.

About programming in JS
-----------------------
For general information on how to use the good parts of JavaScript, see `Crockford's lectures from Yahoo <http://www.yuiblog.com/crockford/>`_. Highly recommended.
