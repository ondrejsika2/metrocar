vagrant up
vagrant ssh -- -t 'cd /home/vagrant/repo/server/metrocar/; sudo a2dissite server.metrocar.jezdito.cz; sudo service apache2 reload; python manage.py runserver 0.0.0.0:8080; /bin/bash'
CMD