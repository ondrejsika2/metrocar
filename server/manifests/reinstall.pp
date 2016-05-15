# default paths to executables
Exec {
  path => [ '/bin/', '/sbin/' , '/usr/bin/', '/usr/sbin/', '/usr/local/bin' ]
}

# class definitions
class { 'postgresql::server': }

# ----- drop database
exec { 'drop_db':
  command => 'psql -c \'drop database if exists metrocar\'',
  cwd => '/home/metrocar/repo/server/',
  user => 'postgres',
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

# ----- re-create db model and load test data

exec { 'py_manage_sync_db':
  command => 'python manage.py syncdb --noinput --settings=metrocar.settings.local',
  cwd => '/home/metrocar/repo/server/metrocar/',
}
->
exec { 'py_manage_dummy_data':
  command => 'python manage.py load_dummy_data',
  cwd => '/home/metrocar/repo/server/metrocar/',
}

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

# ----- restart apache

exec { 'enable_site':
  command => 'a2ensite metrocar.jezdito.cz',
  cwd => "/",
}
->
exec { 'restart_apache':
  command => 'service apache2 reload',
  cwd     => "/",
}