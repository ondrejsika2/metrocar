# default paths to executables
Exec {
  path => [ '/bin/', '/sbin/' , '/usr/bin/', '/usr/sbin/', '/usr/local/bin' ]
}

# ----- checkout vcs

vcsrepo { '/home/metrocar/repo/':
  ensure   => latest,
  provider => git,
  source   => 'https://github.com/tomasj/metrocar.git',
  revision => 'master',
}
->

# ----- rebuild python apps

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

# ----- rebuild client

exec { 'npm_install':
  command => 'npm install',
  cwd => '/home/metrocar/repo/client/',
  user => 'metrocar',
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

# ----- reload apache

exec { 'restart_apache':
  command => 'service apache2 reload',
    cwd => "/",
}
