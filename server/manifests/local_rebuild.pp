# default paths to executables
Exec {
  path => [ '/bin/', '/sbin/' , '/usr/bin/', '/usr/sbin/', '/usr/local/bin' ]
}

# ----- rebuild python apps

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

# ----- rebuild client

exec { 'npm_install':
  command => 'npm install --no-bin-links',
  cwd => '/home/vagrant/repo/client/',
  user => 'vagrant',
  timeout => 1800,
}
->
exec { 'bower_install':
  command => 'bower install --allow-root',
  cwd => '/home/vagrant/repo/client/',
  user => 'vagrant',
}
->
exec { 'ember_build':
  command => 'ember build --no-bin-links --environment=production',
  cwd => '/home/vagrant/repo/client/',
  user => 'vagrant',
}
->

# ----- copy client files to www public folder

file { 'www_folder':
   path => '/var/www/metrocar.jezdito.cz',
   source => '/home/vagrant/repo/client/dist/',
   recurse => true,
}
->

# ----- reload apache

exec { 'restart_apache':
  command => 'service apache2 reload',
    cwd => "/",
}
