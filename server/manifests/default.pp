
# System Packages

$packages = [
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

#package {
#  $packages:
#    ensure => 'installed'
#}


# DB

class { 'postgresql::server': }

postgresql::server::db { 'metrocar2':
  user     => 'metrocar',
  password => postgresql_password('metrocar', 'metrocar_passwd'),
}


# PIP Requirements

#class { 'python': }


vcsrepo { '/home/admin/metrocar':
  ensure   => present,
  provider => git,
  source   => 'git@github.com:tomasj/metrocar.git',
  revision => 'master',
}

->

python::requirements { '/home/admin/metrocar/server/requirements.txt' :
  virtualenv => '/home/admin/.env',
}

