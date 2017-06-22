""" The setuptools module for the Parsing Library """

from codecs import open
from os import path

from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as readme:
    long_description = readme.read()

setup(
    name='sample',
    version='1.0.0',
    description='A mobile application log text parsing library for iOS and Android.',
    long_description=long_description,
    url='https://sumnerevans.github.io/wireless-debugging/',
    author='Sumner Evans',
    author_email='',
    license='Apache Software License',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: Apache Software License',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='log parsing mobile',
    py_modules=['log_parser']
)
