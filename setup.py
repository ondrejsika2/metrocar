from setuptools import setup
import metrocar

setup(
    name='metrocar',
    version=metrocar.__versionstr__,

    packages=('metrocar', 'mfe'),

    include_package_data=True,

    install_requires=(
         'setuptools>=0.6b1',
         'Paver==1.0.5',
     ),
)
