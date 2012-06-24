from paver.easy import *
from paver import doctools


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
