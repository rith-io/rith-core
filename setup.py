#!/usr/bin/env python

"""Arithmetic Geospatial Data API.
"""

from setuptools import setup
from setuptools import find_packages

setup(
    name="rith",
    version="0.0.6",
    description="Arithmetic helps you create production-ready APIs so that your team can build faster, smarter, and more secure.",
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
        "psycopg2"
    ]
)
