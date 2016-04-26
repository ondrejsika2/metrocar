Exec {
  path => [ '/bin/', '/sbin/' , '/usr/bin/', '/usr/sbin/', '/usr/local/bin' ]
}

package {
  'curl':
    ensure => 'installed',
}
->
vcsrepo { '/le':
  provider => git,
  source   => 'https://github.com/lukas2511/letsencrypt.sh.git',
  revision => 'master',
}
->
file {'/le/.acme-challenges':
    ensure => 'directory',
  }
->
exec {'cert_server':
  command => './letsencrypt.sh -c -d server.metrocar.jezdito.cz -t http-01',
  cwd    => '/le',
}
->
exec {'cert_client':
  command => './letsencrypt.sh -c -d metrocar.jezdito.cz -t http-01',
  cwd    => '/le',
}

