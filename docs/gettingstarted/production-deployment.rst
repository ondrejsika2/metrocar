=====================
Production deployment
=====================

------------------------
1. Install prerequisites
------------------------
::

    sudo apt-get install apache2 apache2.2-common apache2-mpm-prefork apache2-utils libexpat1 ssl-cert
    sudo apt-get install libapache2-mod-wsgi
    sudo apt-get install postgresql
    sudo apt-get install postgresql-9.4-postgis-2.1
    sudo apt-get install postgresql-server-dev-9.4
    sudo apt-get install git
    sudo apt-get install python
    sudo apt-get install python-pip
    sudo apt-get install python-dev
    sudo apt-get install virtualenv
    sudo apt-get install npm
    sudo apt-get install nodejs-legacy

-----------------------------
2. Install virtualenvwrapper:
-----------------------------
::

    pip install virtualenvwrapper
    export WORKON_HOME=~/Envs
    mkdir -p $WORKON_HOME
    source /home/metrocar/.local/bin/virtualenvwrapper.sh

----------------------------------
3. Add these command to ~/.bashrc:
----------------------------------
::

    export WORKON_HOME=~/Envs
    source /home/metrocar/.local/bin/virtualenvwrapper.sh


------------------------------
4. Create virtual environment:
------------------------------
::

    mkvirtualenv metrocar

----------------
5. Clone project
----------------
::

    mkdir metrocar
    cd ~/metrocar/wagnejan_metrocar/
    git clone git://git.assembla.com/wagnejan_metrocar.git

----------------------
6. Create certificates
----------------------
::

    mkdir /home/metrocar/cert
    cd /home/metrocar/cert/
    openssl genrsa -des3 -passout pass:x -out server.pass.key 2048
    openssl rsa -passin pass:x -in server.pass.key -out server.key
    rm server.pass.key
    openssl req -new -key server.key -out server.csr
    openssl x509 -req -days 365 -in server.csr -signkey server.key -out server.crt


-----------------------------
7. Deploy server applications
-----------------------------

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
7.1 Create local.py file and edit settings for database
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
::

    cp ~/metrocar/wagnejan_metrocar/server/metrocar/settings/local_example.py ~/metrocar/wagnejan_metrocar/server/metrocar/settings/local.py
    # edit local.py file

~~~~~~~~~~~~~~~~~~~~~
7.2 Build python apps
~~~~~~~~~~~~~~~~~~~~~
::

    cd ~/metrocar/wagnejan_metrocar/server/
    python setup.py sdist
    cd ~/metrocar/wagnejan_metrocar/geotrack/
    python setup.py sdist

~~~~~~~~~~~~~~~~~~~~~~~
7.3 Install python apps
~~~~~~~~~~~~~~~~~~~~~~~
::

    cd ~/metrocar/wagnejan_metrocar/
    pip install geotrack/dist/geotrack-0.0.0.tar.gz
    pip install server/dist/Metrocar-1.0.0.tar.gz

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
7.4 Set up Apache - create file /etc/apache2/sites-available/server.metrocar.knaisl.cz.conf
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
::

    <VirtualHost *:80>
        ServerName server.metrocar.knaisl.cz

        <Directory />
                AllowOverride none
                Require all granted
        </Directory>

        <Directory "/root/">
                Options Indexes FollowSymLinks Includes ExecCGI
                AllowOverride All
                Order deny,allow
                Require all granted
        </Directory>

        WSGIPassAuthorization On
        WSGIDaemonProcess metrocar python-path=/home/metrocar/Envs/metrocar/lib/python2.7/site-packages/
        WSGIProcessGroup metrocar
        WSGIScriptAlias / /home/metrocar/Envs/metrocar/lib/python2.7/site-packages/metrocar/wsgi.py


    </VirtualHost>


~~~~~~~~~~~~~~~~~~~~~~~
7.5 Enable virtual host
~~~~~~~~~~~~~~~~~~~~~~~
::

    sudo a2enmod ssl
    sudo a2ensite server.metrocar.knaisl.cz.conf

~~~~~~~~~~~~~~~~~~~
7.6 Create database
~~~~~~~~~~~~~~~~~~~
- start psql and type these commands:
::

    \c postgres
    DROP DATABASE postgres;
    CREATE DATABASE metrocar;
    \c metrocar
    CREATE EXTENSION postgis;
    CREATE EXTENSION postgis_topology;
    CREATE EXTENSION fuzzystrmatch;
    CREATE EXTENSION postgis_tiger_geocoder;

~~~~~~~~~~~~~~~~~~~~
7.7 Migrate database
~~~~~~~~~~~~~~~~~~~~
::

    cd /home/metrocar/metrocar/wagnejan_metrocar/server/metrocar;
    export DJANGO_SETTINGS_MODULE="metrocar.settings.local"
    python manage.py syncdb
    python manage.py migrate --all
    python manage.py load_dummy_data


~~~~~~~~~~~~~~~~~~~
7.8 Create log file
~~~~~~~~~~~~~~~~~~~
::

    touch /home/metrocar/Envs/metrocar/lib/python2.7/site-packages/metrocar/log/metrocar.log
    chmod 777 /home/metrocar/Envs/metrocar/lib/python2.7/site-packages/metrocar/log/metrocar.log

----------------------------
8. Deploy client application
----------------------------

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
8.1 Install dependencies of client application and buld it
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
::

    cd /home/metrocar/metrocar/wagnejan_metrocar/client
    sudo npm install -g bower
    sudo npm install -g ember-cli
    sudo npm install
    bower install
    ember build --environment=production

~~~~~~~~~~~~~~~~~~~~~~~~~~~~
8.2 Create www public folder
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
::

    mkdir /var/www/metrocar.knaisl.cz
    cd /var/www/metrocar.knaisl.cz
    cp -r /home/metrocar/metrocar/wagnejan_metrocar/client/dist/* ./

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
8.3 Set up Apache - create file /etc/apache2/sites-available/metrocar.knaisl.cz.conf
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
::

    <VirtualHost *:80>
        ServerName metrocar.knaisl.cz
        DocumentRoot /var/www/metrocar.knaisl.cz
        ErrorLog ${APACHE_LOG_DIR}/error.log
        CustomLog ${APACHE_LOG_DIR}/access.log combined

        FallbackResource /index.html

    </VirtualHost>

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
8.4 Enable site and restart Apache
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
::

    sudo a2ensite metrocar.knaisl.cz
    sudo service apache2 reload







