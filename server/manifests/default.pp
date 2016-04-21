Exec {
  path => [ '/bin/', '/sbin/' , '/usr/bin/', '/usr/sbin/' ]
}

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
  'nodejs',
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
        #WSGIDaemonProcess metrocar python-cwd=/home/metrocar/Envs/metrocar/lib/python2.7/site-packages/
        #WSGIProcessGroup metrocar
        #WSGIScriptAlias / /home/metrocar/Envs/metrocar/lib/python2.7/site-packages/metrocar/wsgi.py

        WSGIScriptAlias / /home/metrocar/repo/server/metrocar/wsgi.py
        WSGIPythonPath /home/metrocar/repo/server/metrocar/
    </VirtualHost>',
}

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
  command => '
       bash -c "export DJANGO_SETTINGS_MODULE=metrocar.settings.local; python manage.py syncdb; python manage.py migrate --all;"
    ',
    cwd => '/home/metrocar/repo/server/metrocar/'
}

#exec { 'python_dummy':
#  command => 'python manage.py load_dummy_data',
#  cwd => '/home/metrocar/repo/server/metrocar/'
#}

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
  command => 'npm install',
  cwd => '/home/metrocar/metrocar/wagnejan_metrocar/client/'
}
->
exec { 'bower_install':
  command => 'bower install',
  cwd => '/home/metrocar/metrocar/wagnejan_metrocar/client/'
}
->
exec { 'ember_build':
  command => 'ember build --environment=production',
  cwd => '/home/metrocar/metrocar/wagnejan_metrocar/client/'
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
  command => 'a2ensite metrocar.jezdito.cz',
  cwd => "/",
}
->
exec { 'restart_apache':
  command => 'service apache2 reload',
    cwd => "/",
}

