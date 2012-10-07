import re
from paver.easy import *
from paver import doctools
from paver.path25 import path


options(
    sphinx=Bunch(
        builddir='_build',
    )
)


def managepy(project, cmd):
    sh('python %s/manage.py %s' % (project, cmd))


@task
def install_dependencies():
    """
    Installs required python packages.
    """
    sh('pip install -r requirements.txt')


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
    to create permissions.
    """
    managepy('metrocar', 'migrate')
    managepy('metrocar', 'syncdb --all --noinput')


@task
def deploy():
    sh('git pull')
    delete_pyc()
    # TODO: only run when a new dependency appears
    # install_dependencies()
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
    Symlinks static files from installed apps to STATIC_ROOT
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
