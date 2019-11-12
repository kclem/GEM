from setuptools import setup
import sys

if sys.version_info[0] == 2:
    import ConfigParser as configparser
else:
    import configparser

setup(name='GEM',
        version='1.1',
        package_dir = {'': 'src'},
        py_modules=['GEM','GEM_CRISPOR','GEM_CRISPRESSO'],
        install_requires=[
            'jsonschema',
            'json2html'

        ]
        )
