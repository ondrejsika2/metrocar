==========
Deployment
==========

To deploy the project on the server, currently at rosti_, complete the following
steps:

    1. Log on to the server via SSH (get the login info from
       :ref:`project-maintainer`)::

        $ ssh autonapul.cz

    2. Activate the metrocar virtualenv::

        $ . virtualenvs/metrocar/bin/activate

    3. Go to the metrocar project directory::

        $ cd metrocar

    4. Run the deploy command::

        $ paver deploy


.. _rosti: http://rosti.cz


.. note:: You can make use of the ``screen`` utility to not have to repeat steps
          2 and 3 every time.
