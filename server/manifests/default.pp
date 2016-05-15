# ----- initial config
# symbol -> used to enforce execution order

# default paths to executables
Exec {
  path => [ '/bin/', '/sbin/' , '/usr/bin/', '/usr/sbin/', '/usr/local/bin' ]
}

# class definitions
class { 'postgresql::server': }

# packages var definition
$packages = [
  'apache2',
  'apache2.2-common',
  'apache2-mpm-prefork',
  'apache2-utils',
  'libexpat1',
  'ssl-cert',
  'libapache2-mod-wsgi',
  'postgresql',
  'postgresql-9.4-postgis-2.1',
  'postgresql-server-dev-9.4',
  'git',
  'python',
  'python-pip',
  'python-dev',
  'virtualenv',
  'npm',
  'nodejs',
]

# ----- create user

user{ 'metrocar':
  ensure => 'present',
  password => 'metrocar',
  managehome => true,
}
->

# ----- install packages

package {
  $packages:
    ensure => 'installed',
}
->
file { '/usr/bin/node':
    ensure => 'link',
    target => '/usr/bin/nodejs',
  }
->
# ----- clone git repo

vcsrepo { '/home/metrocar/repo/':
  ensure   => latest,
  provider => git,
  source   => 'https://github.com/tomasj/metrocar.git',
  revision => 'master',
}
->

# ----- create certificates for SSL TODO

# ----- mark default settings file

file { '/home/metrocar/repo/server/metrocar/settings/local.py':
  ensure => 'present',
  source => '/home/metrocar/repo/server/metrocar/settings/local_example.py',
}
->

# ----- build python apps

exec { 'install_geotrack':
  command => 'pip install -e /home/metrocar/repo/geotrack/',
  cwd    => '/home/metrocar/repo/',
}
->
exec { 'install_metrocar':
  command => 'pip install -e /home/metrocar/repo/server/',
  cwd    => '/home/metrocar/repo/',
}
->
exec { 'install_metrocar_requirements':
  command => 'pip install -r /home/metrocar/repo/server/requirements.txt',
  cwd    => '/home/metrocar/repo/',
}
->

# ----- create database

postgresql::server::db { 'metrocar':
  user     => 'metrocar',
  password => postgresql_password('metrocar', 'metrocar'),
}
->
postgresql::server::extension{ 'postgis':
  ensure => 'present',
  database => 'metrocar',
}
->
postgresql::server::extension{ 'postgis_topology':
  ensure => 'present',
  database => 'metrocar',
}
->
postgresql::server::extension{ 'fuzzystrmatch':
  ensure => 'present',
  database => 'metrocar',
}
->
postgresql::server::extension{ 'postgis_tiger_geocoder':
  ensure => 'present',
  database => 'metrocar',
}
->

# ----- apache set up

file{ '/etc/apache2/sites-available/server.metrocar.jezdito.cz.conf':
  ensure => 'present',
  content => '
      <VirtualHost *:80>
        ServerName server.metrocar.jezdito.cz

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
        #WSGIDaemonProcess metrocar python-cwd=/home/metrocar/Envs/metrocar/lib/python2.7/site-packages/
        #WSGIProcessGroup metrocar
        #WSGIScriptAlias / /home/metrocar/Envs/metrocar/lib/python2.7/site-packages/metrocar/wsgi.py

        WSGIScriptAlias / /home/metrocar/repo/server/metrocar/wsgi.py
        #WSGIPythonPath /home/metrocar/repo/server/metrocar/

        Alias /.well-known/acme-challenge /le/.acme-challenges
    </VirtualHost>',
}
->

# ----- enable virtual host

exec { 'a2enmod':
  command => 'a2enmod ssl',
  cwd => "/",
}
->
exec { 'a2ensite':
  command => 'a2ensite server.metrocar.jezdito.cz.conf',
  cwd => "/",
}
->

# ----- setup django

# syncdb
exec { 'py_manage_sync_db':
  command => 'python manage.py syncdb --noinput --settings=metrocar.settings.local',
  cwd => '/home/metrocar/repo/server/metrocar/',
}
->
# first we create a super user using a django shell
exec { 'py_django_su':
  command => 'echo "from django.contrib.auth.models import User; User.objects.create_superuser(\'admin\', \'admin@metrocar.cz\', \'admin\')" | python metrocar/manage.py shell',
  cwd => '/home/metrocar/repo/server/',
}
->
# django site
exec { 'py_django_add_site':
  command => 'echo "from django.contrib.sites.models import Site; site = Site(); site.domain = \'server.metrocar.jezdito.cz\'; site.name = \'server.metrocar.jezdito.cz\'; site.save(); " | python metrocar/manage.py shell',
  cwd => '/home/metrocar/repo/server/',
}
->
# exec { 'py_manage_migrate':
#   command => 'python manage.py migrate --all',
#   cwd => '/home/metrocar/repo/server/metrocar/',
# }
# ->
exec { 'py_manage_dummy_data':
  command => 'python manage.py load_dummy_data',
  cwd => '/home/metrocar/repo/server/metrocar/',
}
->

# ----- install frontend apps

package { 'bower':
  ensure   => 'present',
  provider => 'npm',
}
->
package { 'ember-cli':
  ensure   => 'present',
  provider => 'npm',
}
->
file{'/home/metrocar/repo/client/':
  ensure => 'directory',
  mode => 777,
  owner => 'metrocar',
  seluser => 'metrocar',
  recurse => true,
}
->
file{'/home/metrocar/repo/server/metrocar/log/':
  ensure => 'directory',
  mode => 777,
  owner => 'metrocar',
  seluser => 'metrocar',
  recurse => true,
}
->
exec { 'npm_install':
  command => 'npm install',
  cwd => '/home/metrocar/repo/client/',
  user => 'metrocar',
  timeout => 1800,
}
->
exec { 'bower_install':
  command => 'bower install',
  cwd => '/home/metrocar/repo/client/',
  user => 'metrocar',
}
->
exec { 'ember_build':
  command => 'ember build --environment=production',
  cwd => '/home/metrocar/repo/client/',
  user => 'metrocar',
}
->

# ----- copy client files to www public folder

file { 'www_folder':
   path => '/var/www/metrocar.jezdito.cz',
   source => '/home/metrocar/repo/client/dist/',
   recurse => true,
}
->

# ----- apache setup

file{ '/etc/apache2/sites-available/metrocar.jezdito.cz.conf':
  ensure => 'present',
  content => '
    <VirtualHost *:80>
        ServerName metrocar.jezdito.cz
        DocumentRoot /var/www/metrocar.jezdito.cz
        ErrorLog ${APACHE_LOG_DIR}/error.log
        CustomLog ${APACHE_LOG_DIR}/access.log combined

        <Directory />
            AllowOverride none
            Require all granted
        </Directory>

        FallbackResource /index.html
        Alias /.well-known/acme-challenge /le/.acme-challenges

    </VirtualHost>',
}
->

# ----- enable site and restart apache

exec { 'enable_site':
  command => 'a2ensite metrocar.jezdito.cz',
  cwd => "/",
}
->
exec { 'restart_apache':
  command => 'service apache2 reload',
    cwd => "/",
}

