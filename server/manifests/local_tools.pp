Exec {
  path => [ '/bin/', '/sbin/' , '/usr/bin/', '/usr/sbin/', '/usr/local/bin' ],
  cwd => "/home/vagrant/",
}

# --------------- install webmin

exec { 'update_apt':
  command => 'apt-get -y update',
}
->
exec { 'resolve_webmin_dependencies':
  command => 'apt-get -y install perl libnet-ssleay-perl openssl libauthen-pam-perl libpam-runtime libio-pty-perl apt-show-versions python',
}
->
exec { 'download_webmin_install':
  command => 'wget http://prdownloads.sourceforge.net/webadmin/webmin_1.791_all.deb',
}
->
exec { 'install_webmin':
  command => 'dpkg --install webmin_1.791_all.deb',
}
# for webmin restart use
# /etc/init.d/webmin restart

# ----- puppet modules
# puppet has to be present, use:
# apt-get install puppet

exec { 'puppet_module_1':
  command => 'puppet module install puppetlabs-apache',
}
exec { 'puppet_module_2':
  command => 'puppet module install puppetlabs-postgresql',
}
exec { 'puppet_module_3':
  command => 'puppet module install puppetlabs-vcsrepo',
}
exec { 'puppet_module_4':
  command => 'puppet module install puppetlabs-nodejs',
}

# ----- install phpPgAdmin + adminer

exec { 'phpPgAdmin':
  command => 'apt-get -y install php5-pgsql phppgadmin',
}
->
file{ '/etc/apache2/sites-available/admin.metrocar.jezdito.cz.conf':
  ensure => 'present',
  content => '
      <VirtualHost *:8000>
        ServerName localhost
        DocumentRoot /usr/share/phppgadmin
        DirectoryIndex index.php
      </VirtualHost>',
}
->
file{ '/etc/apache2/conf-available/phppgadmin.conf':
  ensure => 'absent',
}
->
file{ '/etc/apache2/conf-enabled/phppgadmin.conf':
  ensure => 'absent',
}
->
exec { 'a2ensite':
  command => 'a2ensite admin.metrocar.jezdito.cz.conf',
}
->
exec { 'restart_apache':
  command => 'service apache2 reload',
}

# exec { 'adminer':
#   command => 'apt-get -y adminer',
#   cwd => "/root/",
#   path => [ '/bin/', '/sbin/' , '/usr/bin/', '/usr/sbin/' ],
# }