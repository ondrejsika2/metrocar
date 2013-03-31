from setuptools import setup

setup(
    name='accounting',
    version=0.0.1,
    description='Accounting module for carsharing system Metrocar.',
    packages=['accounting'],
    license='BSD',
    author='Jakub Ječmínek',
    author_email='jecmijak@gmail.com',
    keywords='invoices accounting carharing',
    url='https://www.assembla.com/spaces/wagnejan_metrocar/wiki',
    include_package_data=True,

    install_requires=(
         'flexipy',
     ),
)