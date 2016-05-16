# ----- initial config
# symbol -> used to enforce execution order

# default paths to executables
Exec {
  path => [ '/bin/', '/sbin/' , '/usr/bin/', '/usr/sbin/', '/usr/local/bin' ]
}

# class definitions
class { 'postgresql::server': }

# packages var definition
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

# ----- ssl keys

# public key of certificate
$sslInitKey = '-----BEGIN CERTIFICATE-----
MIICWDCCAcGgAwIBAgIJAI/6/vNRKMpZMA0GCSqGSIb3DQEBCwUAMEUxCzAJBgNV
BAYTAkNaMRMwEQYDVQQIDApTb21lLVN0YXRlMSEwHwYDVQQKDBhJbnRlcm5ldCBX
aWRnaXRzIFB0eSBMdGQwHhcNMTYwNTE2MTcxODE3WhcNMjYwNTE0MTcxODE3WjBF
MQswCQYDVQQGEwJDWjETMBEGA1UECAwKU29tZS1TdGF0ZTEhMB8GA1UECgwYSW50
ZXJuZXQgV2lkZ2l0cyBQdHkgTHRkMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKB
gQC0uTROcPIb3/LSgNI15SGJT4C3GU9ahlOFxvRfXNHjPWYYzwR7m/kh7OnVEKHm
EJbeJnL0DKpKAG7ebKm+m6Eykkco4W0m3wcBVnDPz0SJ4fgicnVG3n9hqmgMBATR
ZJz4eFM3QIxM3D767ZXlkLWKAJ3ePw3KZUTmD/6DxuCh2wIDAQABo1AwTjAdBgNV
HQ4EFgQUk77mRWFArC4xPH1gH2gOCAkeuMUwHwYDVR0jBBgwFoAUk77mRWFArC4x
PH1gH2gOCAkeuMUwDAYDVR0TBAUwAwEB/zANBgkqhkiG9w0BAQsFAAOBgQCexUBH
96Eyfg8/nBmD5ucSkgZyYuIOukXhEzZq7pxZgr6vzn/n6/dqkOMEi3YJrTPR16sM
QgtUhTav6n7MaBPQ109DKTFTv82BFKZnJuYGe5H3hH00mfSChSQoBFhzFetKxLpp
JZ/oRL+Ft3MsOpvxK8CHxeKqX3lDMNTzFPi0dQ==
-----END CERTIFICATE-----'

# self signed certificate
$sslInitCert = '-----BEGIN RSA PRIVATE KEY-----
MIICXQIBAAKBgQC0uTROcPIb3/LSgNI15SGJT4C3GU9ahlOFxvRfXNHjPWYYzwR7
m/kh7OnVEKHmEJbeJnL0DKpKAG7ebKm+m6Eykkco4W0m3wcBVnDPz0SJ4fgicnVG
3n9hqmgMBATRZJz4eFM3QIxM3D767ZXlkLWKAJ3ePw3KZUTmD/6DxuCh2wIDAQAB
AoGAQuVnYj3WsNDF7nu21DJbppsiNySMRiMA2b0aig4utyHsH/TJYQQMRS2QJMlC
VIoBfnvXA1WI11mvsG+iqaasFQ/gZP91gKzP3Fdtc5OVUJA9shi5/SyjrBUiNgF6
eraZFjvz9iGd2ZdhXWvgDfSIozg5crjKvKzAHmVA0tMpexkCQQDbnqaH5DyZBVJ+
jxTgEcAxdsJ01Yh5n2RyC7ACK9liFp+Aw9mlzS36zy7pihGFzG7TxRNnF7BbdsTk
9DhVVmJtAkEA0qkXRa4EbjT/4ri+P2EtJMM96//8dXniIhoTba5q/f/wQFcr0iYd
FY6v4SoK7pdYhR0kr/47pM6CBzjEsfYoZwJBAM1GFNGfeyRr3Rd+FTz6WnHhVxBt
JgrH+NLAKdtdsOoFy0BHzv8yMG/lhyuyaX5t/ojiA6iwc56J/K8jtiPNgmECQQCM
dWPn+NRJaxsmX0myVqfT+D4kSgVZis/lLv+/ROlfvDPDopu8Pd9sjTvl5LNvTAgg
kULx+ZBpHawDBq3XfqqHAkAdouVtL+Iq1uGBf3rpiGOJdoGzf/I6SstNBnaOjFjw
6/diF5pCKR2A4L3Xr1PIDGMVvibSd00HpzVXJyfx0Juk
-----END RSA PRIVATE KEY-----'

# ----- create user

user{ 'metrocar':
  ensure => 'present',
  password => 'metrocar',
  managehome => true,
}
->

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
# ----- clone git repo

vcsrepo { '/home/metrocar/repo/':
  ensure   => latest,
  provider => git,
  source   => 'https://github.com/tomasj/metrocar.git',
  revision => 'master',
}
->

# ----- create certificates for SSL TODO

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

# ----- save SSL keys

file{ '/etc/ssl/':
  ensure => 'directory',
}
->
file{ '/etc/ssl/key.pem':
  ensure => 'present',
  content => $sslInitKey,
}
->
file{ '/etc/ssl/cert.pem':
  ensure => 'present',
  content => $sslInitCert,
}
->

# ----- apache set up

file{ '/etc/apache2/sites-available/server.metrocar.jezdito.cz.conf':
  ensure => 'present',
  content => '
      <VirtualHost *:80>
        ServerName server.metrocar.jezdito.cz
        RewriteEngine On
        RewriteRule ^/(.*) https://%{SERVER_NAME}/$1 [L,R]
      </VirtualHost>

      <VirtualHost *:443>
        ServerName server.metrocar.jezdito.cz

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
        #WSGIPythonPath /home/metrocar/repo/server/metrocar/

        Alias /.well-known/acme-challenge /le/.acme-challenges

        SSLEngine on
        SSLCertificateFile /etc/ssl/cert.pem
        SSLCertificateKeyFile /etc/ssl/key.pem
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
  cwd => '/home/metrocar/repo/server/metrocar/',
}
->
# first we create a super user using a django shell
exec { 'py_django_su':
  command => 'echo "from django.contrib.auth.models import User; User.objects.create_superuser(\'admin\', \'admin@metrocar.cz\', \'admin\')" | python metrocar/manage.py shell',
  cwd => '/home/metrocar/repo/server/',
}
->
# django site
exec { 'py_django_add_site':
  command => 'echo "from django.contrib.sites.models import Site; site = Site(); site.domain = \'server.metrocar.jezdito.cz\'; site.name = \'server.metrocar.jezdito.cz\'; site.save(); " | python metrocar/manage.py shell',
  cwd => '/home/metrocar/repo/server/',
}
->
# exec { 'py_manage_migrate':
#   command => 'python manage.py migrate --all',
#   cwd => '/home/metrocar/repo/server/metrocar/',
# }
# ->
exec { 'py_manage_dummy_data':
  command => 'python manage.py load_dummy_data',
  cwd => '/home/metrocar/repo/server/metrocar/',
}
->

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
file{'/home/metrocar/repo/client/':
  ensure => 'directory',
  mode => 777,
  owner => 'metrocar',
  seluser => 'metrocar',
  recurse => true,
}
->
file{'/home/metrocar/repo/server/metrocar/log/':
  ensure => 'directory',
  mode => 777,
  owner => 'metrocar',
  seluser => 'metrocar',
  recurse => true,
}
->
exec { 'npm_install':
  command => 'npm install',
  cwd => '/home/metrocar/repo/client/',
  user => 'metrocar',
  timeout => 1800,
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

# ----- copy client files to www public folder

file { 'www_folder':
   path => '/var/www/metrocar.jezdito.cz',
   source => '/home/metrocar/repo/client/dist/',
   recurse => true,
}
->

# ----- apache setup

file{ '/etc/apache2/sites-available/metrocar.jezdito.cz.conf':
  ensure => 'present',
  content => '
    <VirtualHost *:80>
      ServerName metrocar.jezdito.cz
      RewriteEngine On
      RewriteRule ^/(.*) https://%{SERVER_NAME}/$1 [L,R]
    </VirtualHost>

    <VirtualHost *:443>
        ServerName metrocar.jezdito.cz
        DocumentRoot /var/www/metrocar.jezdito.cz
        ErrorLog ${APACHE_LOG_DIR}/error.log
        CustomLog ${APACHE_LOG_DIR}/access.log combined

        <Directory />
            AllowOverride none
            Require all granted
        </Directory>

        FallbackResource /index.html
        Alias /.well-known/acme-challenge /le/.acme-challenges

        SSLEngine on
        SSLCertificateFile /etc/ssl/cert.pem
        SSLCertificateKeyFile /etc/ssl/key.pem
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

