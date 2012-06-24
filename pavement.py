from paver.easy import *
from paver import doctools
from paver.path25 import path


options(
    sphinx=Bunch(
        builddir='_build',
    )
)


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
