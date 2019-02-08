#!/usr/bin/env python

"""Arith Geospatial Data API.
"""

from setuptools import setup

setup(
    name="rith",
    version="0.0.2",
    description="An open-source geospatial API",
    url="https://github.com/joshuapowell/arith",
    author="Joshua Powell",
    license="MIT",
    keywords="python geospatial location api",
    packages=["rith"],
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
