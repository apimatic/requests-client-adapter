# -*- coding: utf-8 -*-

import sys
from setuptools import setup, find_packages

if sys.version_info[0] < 3:
    with open('README.md', 'r') as fh:
        long_description = fh.read()
else:
    with open('README.md', 'r', encoding='utf-8') as fh:
        long_description = fh.read()

setup(
    name='apimatic-requests-client-adapter',
    version='1.0.0',
    description='The implementation of Requests client library provided by APIMatic',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='APIMatic',
    author_email='support@apimatic.io',
    url='https://apimatic.io',
    packages=find_packages(),
    # package_data={"core": ["py.typed"]},
    install_requires=[
        'requests~=2.25',
        'cachecontrol~=0.12.6'
    ],
    tests_require=[
        'pytest~=7.1.3',
        'pytest-cov~=3.0.0'
    ]
)
