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