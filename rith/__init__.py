"""Arithmetic Framework.

Created by Joshua Powell on 02/02/2019.

Copyright (c) 2019 Joshua Powell, L.L.C. All rights reserved.

For license and copyright information please see the LICENSE.md (the "License")
document packaged with this software. This file and all other files included in
this packaged software may not be used in any manner except in compliance with
the License. Software distributed under this License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTY, OR CONDITIONS OF ANY KIND, either express or
implied.

See the License for the specific language governing permission and limitations
under the License.
"""


__author__ = 'Joshua I. Powell'
__copyright__ = 'Copyright 2017 Joshua Powell, L.L.C. All rights reserved.'
__date__ = '2019-02-02'
__license__ = 'MIT'
__organization__ = 'Joshua Powell, L.L.C.'
__status__ = 'Production'
__version__ = '1.0.0'


import flask
import imp
import logging
import os


from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security
from flask_oauthlib.provider import OAuth2Provider


from . import responses


"""System Logging.

System logging enables us to retain useful activity within the system in
server logs. Log messages are written to the Terminal or Application Runner
(e.g., Supervisor) server logs.

Below sets up the `basicConfig` which opens a stream that allows us to add
formatted log messages to the root logger.

@param (object) logger
    Provides the ability to write directly to the logger with the info(),
    warning(), error(), and critical() methods

See the official Python::logging documentation for more Information
https://docs.python.org/2/library/logging.html
"""
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


"""Setup Database.

Initializes the object relational mapper (ORM) that allows the application to
communicate directly with the database.

:param object db:
    The instantiated SQLAlchemy instance

See the official SQLAlchemy documentation for more information
http://docs.sqlalchemy.org/en/latest/
"""
db = SQLAlchemy()


"""OAuth Authorization.

Initializes OAuth authorization support used throughout the system for access
to endpoints and system functionality.

See the official OAuthLib documentation for more information
https://flask-oauthlib.readthedocs.io/en/latest/
"""
oauth = OAuth2Provider()


"""Consisitent System-wide Responses.
Initializes Viable's Response library for returning consistent HTTP Responses
in JSON format.
No official documentation yet exists.
"""
responses = responses.Responses()


def create_application(environment='production'):
    """Production Application Runner."""
    from . import application
    from . import errors

    """Instantiate the Application

    Setup the basic Application class in order to instantiate the rest of
    the Application

    @param (str) name
        The name of the Application
    @param (str) envioronment
        The desired environment configuration to start the application on
    """
    instance = application.Application(
        name="__main__",
        environment=environment
    )

    """Instaniate App-level error handling

    :param object app: Instantiated app object
    """
    errors = errors.ErrorHandlers(instance.app)
    errors.load_errorhandler(instance.app)

    return instance.app
