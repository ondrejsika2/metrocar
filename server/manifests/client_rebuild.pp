# ----- initial config
# symbol -> used to enforce execution order

# default paths to executables
Exec {
  path => [ '/bin/', '/sbin/' , '/usr/bin/', '/usr/sbin/', '/usr/local/bin' ],
}

# ----- recompile frontend

exec { 'ember_build':
  environment => ["HOME=/home/metrocar/"],
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