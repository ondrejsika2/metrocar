# ----- create user

user{ 'metrocar':
  ensure => 'present',
  password => 'metrocar'
}

# ----- install packages

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
  'nodejs-legacy',
]

package {
  $packages:
    ensure => 'installed'
}

# ----- clone git repo

vcsrepo { '/home/metrocar/repo/':
  ensure   => present,
  provider => git,
  source   => 'https://github.com/tomasj/metrocar.git',
}

# ----- create certificates for SSL TODO

file { '/home/metrocar/repo/server/metrocar/settings/local.py':
  ensure => 'present',
  source => '/home/metrocar/repo/server/metrocar/settings/local_example.py'

}

# ----- build python apps

exec { 'install_geotrack':
  command => 'pip install geotrack/dist/geotrack-0.0.0.tar.gz',
  path    => '/home/metrocar/repo/',
}
->
exec { 'install_metrocar':
  command => 'pip install server/dist/Metrocar-1.0.0.tar.gzz',
  path    => '/home/metrocar/repo/',
}

# ----- apache set up

file{ '/etc/apache2/sites-available/server.metrocar.jezdito.cz.conf':
  ensure => 'present',
  content => '
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


    </VirtualHost>',
}

# ----- enable virtual host

exec { 'a2enmod':
  command => 'sudo a2enmod ssl',
}
->
exec { 'a2ensite':
  command => 'sudo a2ensite server.metrocar.jezdito.cz.conf',
}

# ----- create database

class { 'postgresql::server': }

postgresql::server::db { 'metrocar':
  user     => 'metrocar',
  password => postgresql_password('metrocar', 'metrocar'),
}

postgresql::server::extension{ 'postgis':
  ensure => 'present',
  database => 'metrocar',
}

postgresql::server::extension{ 'postgis_topology':
  ensure => 'present',
  database => 'metrocar',
}

postgresql::server::extension{ 'fuzzystrmatch':
  ensure => 'present',
  database => 'metrocar',
}

postgresql::server::extension{ 'postgis_tiger_geocoder':
  ensure => 'present',
  database => 'metrocar',
}

# ----- create database

exec { 'export_settings_module':
  command => 'export DJANGO_SETTINGS_MODULE="metrocar.settings.local',
  path => '/home/metrocar/repo/server/metrocar/'
}

exec { 'python_syncdb':
  command => 'python manage.py syncdb',
  path => '/home/metrocar/repo/server/metrocar/'
}

exec { 'python_migrate':
  command => 'python manage.py migrate --all',
  path => '/home/metrocar/repo/server/metrocar/'
}

exec { 'python_dummy':
  command => 'python manage.py load_dummy_data',
  path => '/home/metrocar/repo/server/metrocar/'
}

# ----- create log file TODO needed?

# ----- install frontend apps

package { 'bower':
  ensure   => 'present',
  provider => 'npm',
}

package { 'ember-cli':
  ensure   => 'present',
  provider => 'npm',
}

exec { 'npm_install':
  command => 'sudo npm install',
  path => '/home/metrocar/metrocar/wagnejan_metrocar/client/'
}
->
exec { 'bower_install':
  command => 'bower install',
  path => '/home/metrocar/metrocar/wagnejan_metrocar/client/'
}
->
exec { 'ember_build':
  command => 'ember build --environment=production',
  path => '/home/metrocar/metrocar/wagnejan_metrocar/client/'
}

# ----- www public folder

file { 'www_folder':
   path => '/var/www/metrocar.jezdito.cz',
   source => '/home/metrocar/metrocar/repo/client/dist/',
   recurse => true,
}

# ----- apache setup

file{ '/etc/apache2/sites-available/metrocar.jezdito.cz.conf':
  ensure => 'present',
  content => '
    <VirtualHost *:80>
        ServerName metrocar.jezdito.cz
        DocumentRoot /var/www/metrocar.jezdito.cz
        ErrorLog ${APACHE_LOG_DIR}/error.log
        CustomLog ${APACHE_LOG_DIR}/access.log combined

        FallbackResource /index.html

    </VirtualHost>',
}

# ----- enable site and restart apache

exec { 'enable_site':
  command => 'sudo a2ensite metrocar.jezdito.cz'
}
->
exec { 'restart_apache':
  command => 'sudo service apache2 reload'
}
