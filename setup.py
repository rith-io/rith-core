#!/usr/bin/env python

"""Arith Geospatial Data API.
"""

from setuptools import setup

setup(
    name="arith",
    version="0.0.1",
    description="An open-source geospatial API",
    url="https://github.com/joshuapowell/arith",
    author="Joshua Powell",
    license="MIT",
    keywords="python geospatial location api",
    packages=["arith"],
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
