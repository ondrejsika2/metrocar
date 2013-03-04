==========
Deployment
==========

The project is currently hosted at rosti_. The project consists of two application, therefore you have to deploy theme seperately, this is the way how application deployment is recomended by rosti documentation.To deploy the project, complete the following
steps:

 

    1. Log on to the server via SSH (get the login info from
       :ref:`project-maintainer`)::

        $ ssh -l <username> pandora.rosti.cz 


        username is different for both applications:
        - mfe(autonapul.cz) has username app_00009
        - metrocar(admin.autonapul.cz) has username app_00008

    2. Activate the metrocar virtualenv::

        $ . venv/bin/activate

    3. Go to the metrocar project directory::

        $ cd metrocar

    4. Run the deploy command::

        $ paver deploy

    5. Restart application from rosti_ web interface   


.. _rosti: http://rosti.cz


.. note:: You can make use of the ``screen`` utility to not have to repeat steps
          2 and 3 every time.
