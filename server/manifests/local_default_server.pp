# ----- initial config
# symbol -> used to enforce execution order

# default paths to executables
Exec {
  path => [ '/bin/', '/sbin/' , '/usr/bin/', '/usr/sbin/', '/usr/local/bin' ],
}

# class definitions
class { 'postgresql::server': }


# install apache support packages in specific version
# package { 'apache2.2-bin':
#   ensure => '2.2.22-1ubuntu1.10',
# }
# package { 'apache2.2-common':
#   ensure => '2.2.22-1ubuntu1.10',
# }
# package { 'apache2.2-common':
#   ensure => '2.2.22-1ubuntu1.10',
# }

# packages var definition
# note: postgres downgraded to 9.3 to ensure Ubuntu 14 (OS) compatibility
$packages = [
  'apache2',
  'apache2-mpm-prefork',
  'apache2-utils',
  'libexpat1',
  'ssl-cert',
  'libapache2-mod-wsgi',
  'postgresql',
  'postgresql-9.3-postgis-2.1',
  'postgresql-server-dev-9.3',
  'git',
  'python',
  'python-pip',
  'python-dev',
  #'virtualenv',
  'npm',
  'nodejs',
]

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

# ----- create certificates for SSL TODO

# ----- mark default settings file

file { '/home/vagrant/repo/server/metrocar/settings/local.py':
  ensure => 'present',
  source => '/home/vagrant/repo/server/metrocar/settings/local_example.py',
}
->

# ----- build python apps

exec { 'install_geotrack':
  command => 'pip install -e /home/vagrant/repo/geotrack/',
  cwd    => '/home/vagrant/repo/',
}
->
exec { 'install_metrocar':
  command => 'pip install -e /home/vagrant/repo/server/',
  cwd    => '/home/vagrant/repo/',
}
->
exec { 'install_metrocar_requirements':
  command => 'pip install -r /home/vagrant/repo/server/requirements.txt',
  cwd    => '/home/vagrant/repo/',
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
      Listen 8080
      <VirtualHost *:8080>
        ServerName localhost

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
        #WSGIDaemonProcess metrocar python-cwd=/home/vagrant/Envs/metrocar/lib/python2.7/site-packages/
        #WSGIProcessGroup metrocar
        #WSGIScriptAlias / /home/vagrant/Envs/metrocar/lib/python2.7/site-packages/metrocar/wsgi.py

        WSGIScriptAlias / /home/vagrant/repo/server/metrocar/wsgi.py
        #WSGIPythonPath /home/vagrant/repo/server/metrocar/

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
  cwd => '/home/vagrant/repo/server/metrocar/',
}
->
# first we create a super user using a django shell
exec { 'py_django_su':
  command => 'echo "from django.contrib.auth.models import User; User.objects.create_superuser(\'admin\', \'admin@metrocar.cz\', \'admin\')" | python metrocar/manage.py shell',
  cwd => '/home/vagrant/repo/server/',
}
->
# django site
exec { 'py_django_add_site':
  command => 'echo "from django.contrib.sites.models import Site; site = Site(); site.domain = \'server.metrocar.jezdito.cz\'; site.name = \'server.metrocar.jezdito.cz\'; site.save(); " | python metrocar/manage.py shell',
  cwd => '/home/vagrant/repo/server/',
}
->
# exec { 'py_manage_migrate':
#   command => 'python manage.py migrate --all',
#   cwd => '/home/vagrant/repo/server/metrocar/',
# }
# ->
exec { 'py_manage_dummy_data':
  command => 'python manage.py load_dummy_data',
  cwd => '/home/vagrant/repo/server/metrocar/',
}
# ->