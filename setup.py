import os
import sys

from setuptools import setup

test_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, test_dir)

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='testmaker',
    version='0.1',
    packages=['testmaker'],
    include_package_data=True,
    license='BSD License',
    description='A simple multiple-choice tests application',
    url='https://github.com/aherok/testmaker',
    author='Andrzej Herok',
    author_email='andrzej@herok.pl',
    install_requires = [
        'Django==1.6.5',
        'South==1.0',
        'psycopg2==2.5.3',
        'django-registration==1.0',
      ],
    test_suite='runtests.runtests',
)
