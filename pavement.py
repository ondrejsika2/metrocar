import re
import os
from functools import partial

from paver import doctools
from paver.easy import options, Bunch, task, sh
from paver.path25 import path


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
        return

    sh('pip install -r ' + requirements_file)

    # remember what was installed
    with open(installed_file, 'w+') as f:
        f.write(requirements)


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

    for project in 'metrocar', 'mfe':
        managepy(project, 'collectstatic -v0 --noinput --link')


@task
def test():
    """
    Run the test-suite.
    """
    sh('python tests/testproject/run_tests.py')


@task
def convert_to_south():
    managepy('metrocar', 'syncdb')

    for app in (
        'cars',
        'invoices',
        'reservations',
        'subsidiaries',
        'tariffs',
        'tarification',
        'user_management',
        'utils',
        'utils.flatpagesmeta',
    ):
        managepy('metrocar', 'migrate %s 0001 --fake' % app)


@task
def blankdb():
    """
    Drop database and start with a fresh one (with testing data loaded).

    Intended for development. You're probably going to need to put something
    like this into your pg_hba.conf::

        local    all    all    trust
    """
    import metrocar.settings
    db_settings = metrocar.settings.DATABASES['default']

    # drop the old one
    sh('dropdb -U %(USER)s %(NAME)s' % db_settings, ignore_error=True)

    # create a new one
    sh("""psql -U %(USER)s << EOF

    CREATE DATABASE %(NAME)s
      WITH ENCODING='UTF8'
           OWNER=%(USER)s
           TEMPLATE=template_postgis
           CONNECTION LIMIT=-1;
    """ % db_settings)

    # populate it with some data
    map(partial(managepy, 'metrocar'), [
        'syncdb --all --noinput',
        'migrate --fake',
        'load_dummy_data',
    ])
