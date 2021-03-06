import re
import os
from functools import partial

from paver import doctools
from paver.easy import options, Bunch, task, sh, BuildFailure
from paver.path25 import path, pushd


options(
    sphinx=Bunch(
        builddir='_build',
    )
)


def managepy(project, cmd):
    sh('python %s/manage.py %s' % (project, cmd))


def read_requirements(filename):
    """
    Read pip requirements file and return it's canonical form in a string
    -- without unnecessary whitespace, comments and sorted alphabetically.
    """
    strip_whitespace = partial(map, str.strip)
    remove_empty_lines = partial(filter, None)
    strip_comments = partial(filter, lambda line: not line.startswith('#'))
    return (
        '\n'.join(
        sorted(
        strip_comments(
        remove_empty_lines(
        strip_whitespace(
        open(filename)))))))


@task
def install_dependencies():
    """
    Installs required python packages.

    Only install if the requirements file changed.
    """
    requirements_file = 'requirements.txt'
    installed_file = 'requirements.installed'
    requirements = read_requirements(requirements_file)
    installed = os.path.exists(installed_file) and open(installed_file).read()
    if installed == requirements:
        print ('Nothing new to install. Delete %s if you want to try anyway' %
            installed_file)
    else:
        sh('pip install -r ' + requirements_file)

        # remember what was installed
        with open(installed_file, 'w+') as f:
            f.write(requirements)
    try:
        import geotrack
    except ImportError:
        # geotrack should probably have it's own repository.....
        with pushd('geotrack'):
            sh('python setup.py develop')


@task
def delete_pyc():
    """
    Delete all *.pyc files recursively from this directory.
    """
    for file in path('.').walkfiles('*.pyc'):
        file.remove()


@task
def uwsgi_restart():
    for pid in re.findall('run (\d+):', sh('uwsgi-manager -l', capture=True)):
        sh('uwsgi-manager -R ' + pid)


@task
def update_db():
    """
    Updates database schema by running South migrations and syncdb --all
    """
    managepy('metrocar', 'migrate')
    managepy('metrocar', 'syncdb --all --noinput')


@task
def deploy():
    sh('git pull')
    delete_pyc()
    install_dependencies()
    update_db()
    collectstatic()
    uwsgi_restart()
    build_docs()


@task
def build_docs():
    doctools.doc_clean()
    doctools.html()
    # also build docs for Geotrack
    with pushd('geotrack/docs'):
        sh('make clean && make html')


@task
def collectstatic():
    """
    Symlinks static files from installed apps to STATIC_ROOT.

    (Generally not needed in development)
    """
    # TODO: get static root from settings
    STATIC_ROOT = 'static'

    # delete old static files, because sometimes the collecstatic
    # command complains about them already existing, for some reason...
    sh('rm -rf %s/*' % STATIC_ROOT)

    managepy('metrocar', 'collectstatic -v0 --noinput --link')


@task
def test():
    """
    Run the test-suite.
    """
    load_settings()
    from metrocar.settings.local import DATABASES
    build_db(DATABASES['testing'])

    load_settings_for_testing()
    sh('python test_metrocar/run_tests.py')

def dropdb(db_settings):

    def drop_postgis(db_settings):
        sh('dropdb -U %(USER)s "%(NAME)s"' % db_settings, ignore_error=True)
        sh("""psql -U %(USER)s postgres << EOF

        CREATE DATABASE "%(NAME)s"
          WITH ENCODING='UTF8'
               OWNER="%(USER)s"
               TEMPLATE=template_postgis
               CONNECTION LIMIT=-1;
        """ % db_settings)

    def drop_sqlite(db_settings):
        try:
            os.remove(db_settings['NAME'])
        except OSError:
            pass

    recipes = {
        'django.db.backends.sqlite3': drop_sqlite,
        'django.contrib.gis.db.backends.postgis': drop_postgis
    }

    engine = db_settings['ENGINE']
    if engine not in recipes:
        raise BuildFailure("Sorry, don't know how to drop %s" % engine)

    recipes[engine](db_settings)

def load_settings():
    DJANGO_SETTINGS_MODULE = 'metrocar.settings.local'
    os.environ['DJANGO_SETTINGS_MODULE'] = DJANGO_SETTINGS_MODULE

def load_settings_for_testing():
    DJANGO_SETTINGS_MODULE = 'test_metrocar.settings.local'
    os.environ['DJANGO_SETTINGS_MODULE'] = DJANGO_SETTINGS_MODULE


def build_db(DATABASE):
    dropdb(DATABASE)
    map(partial(managepy, 'metrocar'), [
        'syncdb --all --noinput',
        'migrate --fake',

    ])

@task
def blankdb():
    """
    Drop database and start with a fresh one (with testing data loaded).

    Intended for development. You're probably going to need to put something
    like this into your pg_hba.conf::

        local    all    all    trust
    """
    load_settings()
    from metrocar.settings.local import DATABASES
    build_db(DATABASES['default'])
    managepy('metrocar', 'load_dummy_data',)
