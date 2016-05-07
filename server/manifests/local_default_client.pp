# ----- initial config
# symbol -> used to enforce execution order

# default paths to executables
Exec {
  path => [ '/bin/', '/sbin/' , '/usr/bin/', '/usr/sbin/', '/usr/local/bin' ],
}

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
package { 'symlink-or-copy':
  ensure   => 'present',
  provider => 'npm',
}
->
package { 'copy-dereference':
  ensure   => 'present',
  provider => 'npm',
}
->
file{'/home/vagrant/repo/client/':
  ensure => 'directory',
  mode => 777,
  owner => 'vagrant',
  seluser => 'vagrant',
  recurse => true,
}
->
file{'/home/vagrant/repo/server/metrocar/log/':
  ensure => 'directory',
  mode => 777,
  owner => 'vagrant',
  seluser => 'vagrant',
  recurse => true,
}
->
file{'/home/vagrant/repo/client/node_modules/':
  ensure => 'absent',
  recurse => true,
  purge => true,
  force => true,
}
->
file{'/home/vagrant/repo/client/bower_components/':
  ensure => 'absent',
  recurse => true,
  purge => true,
  force => true,
}
->
exec { 'npm_install':
  command => 'npm install --no-bin-links',
  cwd => '/home/vagrant/repo/client/',
  user => 'vagrant',
  timeout => 1800,
}
->
exec { 'bower_install':
  environment => ["HOME=/home/vagrant/"],
  command => 'bower install --allow-root',
  cwd => '/home/vagrant/repo/client/',
  user => 'vagrant',
}
->
exec { 'ember_build':
  environment => ["HOME=/home/vagrant/"],
  command => 'ember build --environment=local',
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

# ----- apache setup

file{ '/etc/apache2/sites-available/metrocar.jezdito.cz.conf':
  ensure => 'present',
  content => '
    <VirtualHost *:80>
        ServerName localhost
        DocumentRoot /var/www/metrocar.jezdito.cz
        ErrorLog ${APACHE_LOG_DIR}/error.log
        CustomLog ${APACHE_LOG_DIR}/access.log combined

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

