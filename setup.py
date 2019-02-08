#!/usr/bin/env python

"""Arithmetic Geospatial Data API.
"""


import io
from setuptools import setup
from setuptools import find_packages


with io.open('README.rst', 'rt', encoding='utf8') as f:
    readme = f.read()


setup(
    name="rith",
    version="0.0.10",
    description="Arithmetic helps you create production-ready APIs so that your team can build faster, smarter, and more secure.",
    long_description=readme,
    url="https://github.com/rith-io/rith-core",
    author="Joshua Powell",
    license="MIT",
    keywords="python geospatial location api",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "flask",
        "flask-security",
        "flask-restless",
        "flask-sqlalchemy",
        "geoalchemy2",
        "flask-oauthlib",
        "requests",
        "psycopg2-binary",
        "Wand"
    ],
    extras_require={
        'dev': [
            'bandit',
            'nose',
            'pycodestyle',
            'pydocstyle',
            'pylint',
            'tox',
            'twine',
        ],
        'docs': []
    },
)
