"""Arithmetic Application Class.

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


import io
import json


from datetime import datetime


from flask import jsonify
from flask import request
from flask_restless import APIManager
from flask_security.signals import user_registered


from . import db
from . import flask
from . import imp
from . import logger
from . import logging
from . import Mail
from . import oauth
from . import os
from . import Security


CORE_MODULES = [
    'core',
    'oauth',
]


SYSTEM_FILES = [
    '__init__.py',
    '__pycache__'
]


class Application(object):
    """Create Flask Application via a Class."""

    def __init__(self, environment, name, app=None, extensions={}):
        """Application Constructor.

        Setup our base Flask application, retaining it as our application
        object for use throughout the application

        :param (class) self
            The representation of the instantiated Class Instance
        :param (str) name
            The name of the application
        :param (str) environment
            The name of the enviornment in which to load the application
        :param (class) app
            The Flask class for the application that was created
        """
        logger.info('Application Started at %s', datetime.utcnow())

        self.name = name
        self.environment = environment
        self.extensions = extensions

        """Create our base Flask application
        """
        logger.info('Starting application named `%s`' % __name__)
        self.app = flask.Flask(__name__)

        """Import all custom app configurations
        """
        _config = ('config/%s.config') % (environment)

        """Read the JSON configuration file content.
        """
        logger.info('Application loading configuration from %s', _config)
        self.app.config.from_json(_config)

        """Setup Cross Site Origin header rules
        """
        self.app.after_request(self.setup_default_cors)

        self.manager = APIManager(self.app, flask_sqlalchemy_db=db)

        """Load system extensions
        """
        self.load_extensions()

        """Setup the Database
        """
        self.setup_database()

        """Load system modules
        """
        self.load_modules()

        """Setup the Diagnostics
        """
        self.setup_diagnostics()

        logger.info('Application setup complete')

    def setup_diagnostics(self):
        """Define automated error reporting tools.

        :param (object) self
            the current class (i.e., Application)

        @return (None)
        """
        logger.info('Application searching for automated error reporting')

        # if 'SENTRY_DSN' in self.app.config:
        #     sentry.init_app(self.app, dsn=self.app.config['SENTRY_DSN'],
        #                     logging=True, level=logging.ERROR)
        #     logger.info("Application has successfully loaded Sentry")

    def setup_default_cors(self, response):
        r"""Define global Cross Origin Resource Sharing rules.

        Setup our headers so that the respond correctly and securely

        :param (object) self
            the current class (i.e., Application)

        @return (object) response
            the fully qualified response object
        """
        logger.info('Application Cross Origin Resource Sharing')

        """Access-Control-Allow-Origin
        """
        _origin = None

        if flask.request.headers.get('Origin', '') in \
                self.app.config['ACCESS_CONTROL_ALLOW_ORIGIN']:
            _origin = request.headers.get('Origin', '')

        """Access-Control-Allow-Methods
        """
        _methods = self.app.config['ACCESS_CONTROL_ALLOW_METHODS']

        """Access-Control-Allow-Headers
        """
        _headers = self.app.config['ACCESS_CONTROL_ALLOW_HEADERS']

        """Access-Control-Allow-Credentials
        """
        _credentials = self.app.config['ACCESS_CONTROL_ALLOW_CREDENTIALS']

        """Setup Access Control headers for the application

        Using the user defined enviornment, setup access control headers
        """
        response.headers['Access-Control-Allow-Origin'] = _origin
        response.headers['Access-Control-Allow-Methods'] = _methods
        response.headers['Access-Control-Allow-Headers'] = _headers
        response.headers['Access-Control-Allow-Credentials'] = _credentials

        return response

    def load_extensions(self):
        r"""Define reusable extensions throughout the main application.

        Setup system extensions that are critical to the secure operation of
        this application

        :param (object) self
            the current class (i.e., Application)
        """
        logger.info('Application is loading extensions')

        """Setup Mail

        See the official Flask Mail documentation for more information
        https://pythonhosted.org/Flask-Mail/
        """
        if self.app.config['MODULE_MAIL_ENABLED']:
            self.extensions['mail'] = Mail()
            self.extensions['mail'].init_app(self.app)

        """Setup OAuth 2.0

        See the official Flask OAuthlib documentation for more information
        https://flask-oauthlib.readthedocs.org/en/latest/
        """
        if self.app.config['MODULE_OAUTH_ENABLED']:
            oauth.init_app(self.app)

        """Setup Security

        @todo it is possible that we will want to incorporate this into it's
        own module so that it is not instantiated until a little later OR
        at least until we import our own "Security" module
        """
        if self.app.config['MODULE_SECURITY_ENABLED']:
            from app.schema.user import user_datastore

            self.extensions['security'] = Security()
            self.extensions['security'].init_app(self.app, user_datastore)

            self.assign_default_user_role(self.app, db, user_datastore,
                                          'generic')

    def setup_database(self):
        r"""Create all database tables."""
        logger.info('Application is setting up database')

        db.app = self.app
        db.init_app(self.app)

        """Create all database tables

        Create all of the database tables defined with the modules.
        """
        db.create_all()

    def assign_default_user_role(self, app, db, user_datastore, role):
        r"""Ensure that users are assigned the app-defined role by default.

        :param object app
            the application we are acting upon
        :param object db
            the database our application is using for storage
        :param object user_datastore
            the Flask Security User Datastore implementation
        :param string role
            the name of the `Role` we want to assign by default
        """
        @user_registered.connect_via(app)
        def user_registered_sighandler(app, user, confirm_token):
            """Retrieve the default role requested."""
            default_role = user_datastore.find_role(role)

            """Assign that role to the acting `User` object."""
            user_datastore.add_role_to_user(user, default_role)

            """Save all of our revisions to the database."""
            db.session.commit()

    def load_endpoint(self, Module):
        r"""Load a single module endpoint.

        Given a module name, locate the `endpoint.py` file, and instantiate a
        new Flask Restless compatible endpoint accorindg to the settings
        contained within the `endpoint.py` file.

        :param object self: The Application class
        :param object Module: The of module containing endpoint

        See the official Flask Restless documentation for more information
        https://flask-restless.readthedocs.org/en/latest/api.html#\
        flask_restless.APIManager.create_api
        """
        if hasattr(Module, 'endpoints'):
            """Legacy Support."""

            if hasattr(Module, 'Model'):

                module_arguments = Module.endpoints.Seed().__arguments__

                with self.app.app_context():
                    self.manager.create_api(Module.Model, **module_arguments)
                    logger.info('`%s` module endpoints loaded' %
                                (Module.__name__))
            else:
                logger.error('`%s` module has endpoints, but is missing '
                             'Model' % (Module.__name__))
        elif hasattr(Module, '__arguments__'):
            """Version 1.0 Support."""

            if hasattr(Module, 'Model'):

                module_arguments = Module.__arguments__

                with self.app.app_context():
                    self.manager.create_api(Module.Model, **module_arguments)
                    logger.info('`%s` module endpoints loaded' %
                                (Module.__name__))
            else:
                logger.error('`%s` module has endpoints, but is missing '
                             'Model' % (Module.__name__))
        else:
            logger.info('`%s` module did not contain any endpoints.' %
                        (Module.__name__))

    def load_architecture(self, Module):
        r"""Load the architecture for a single module.

        Given a module name, locate and describe the Model, and instantiate a
        new architecture pattern to inform user interfaces of how to use
        the data model.

        :param object self: The Application class
        :param object Module: The of module containing endpoint
        """
        if hasattr(Module, 'Model') and hasattr(Module.Model, '__def__'):

            filename_ = str(Module.Model.__tablename__)
            filepath_ = ('rith/static/models/%s.json') % (filename_)
            filedata_ = {
                "machine_name": filename_,
                "display_name": Module.Model.__name__,
                "access": Module.Model.__def__.get('access'),
                "fields": Module.Model.__def__.get('fields'),
                "groups": Module.Model.__def__.get('groups'),
            }

            with io.open(filepath_, "w", encoding="utf-8") as file_:
                data_ = json.dumps(filedata_, ensure_ascii=False, indent=4)
                file_.write(str(data_))

            return filedata_

        else:
            logger.info('`%s` module did not contain any model definitions.' %
                        (Module.__name__))

    def load_modules(self):
        """Load all application modules.

        Open the module path defined in the configuration, for each module
        directory found in the defined module path we need to `load_module`,
        and create a Flask Blueprint with the module information.

        :param (object) self
            the current class (i.e., Application)
        """
        logger.info('Application beginning to load modules')

        modules_path = self.app.config['MODULE_PATH']
        modules_directory = os.listdir(modules_path)

        modules_list = {}
        definition_list = []

        for module_name in modules_directory:

            module_path = os.path.join(modules_path, module_name)
            module_package = os.path.join(modules_path, module_name,
                                          '__init__.py')

            if os.path.isdir(module_path) and \
               module_name not in SYSTEM_FILES:

                """Locate and load the module into our module_list
                """
                try:
                    f, filename, descr = imp.find_module(module_name,
                                                         [modules_path])

                    modules_list[module_name] = imp.load_module(module_name,
                                                                f, filename,
                                                                descr)
                except ImportError:
                    logger.error('`load_modules` was unable to locate the'
                                 '`__init__.py` file in your %s module' %
                                 (module_name))
                    raise

                """Register this module with the application as a blueprint

                See the official Flask API for more information about Blueprint
                http://flask.pocoo.org/docs/0.10/api/#flask.Flask.register_blueprint
                """
                if hasattr(modules_list[module_name], 'module'):
                    module_blueprint = modules_list[module_name].module
                    self.app.register_blueprint(module_blueprint)

                    logger.info('Application successfully loaded `%s` module' %
                                (module_name))

                    """Load any endpoints contained within this module.

                    Use the Application.load_endpoint method to instantiate any
                    endpoints contained within the module.
                    """
                    self.load_endpoint(modules_list[module_name])

                    """Load any architecture patterns that are contained within
                    this module.

                    Use the Application.load_architecture method to instantiate
                    any architecture descriptions within the module.
                    """
                    if module_name not in CORE_MODULES:
                        logger.info('Applicaton loading non-core architecture '
                                    'pattern')
                        module_to_load_ = modules_list[module_name]
                        definition_ = self.load_architecture(module_to_load_)
                        if definition_:
                            definition_list.append(definition_)

                else:
                    logger.error('Application failed to load `%s` module' %
                                 (module_name))

        """Create a single structure file that can be served to include
        information about this application.
        """
        filepath_ = ('rith/static/models/all.json')
        filedata_ = {
            "application": {
                "name": self.app.config['APP_NAME'],
                "description": self.app.config['APP_DESCRIPTION'],
                "license": self.app.config['APP_LICENSE'],
                "version": self.app.config['APP_VERSION'],
            },
            "templates": definition_list
        }

        with io.open(filepath_, "w", encoding="utf-8") as file_:
            data_ = json.dumps(filedata_, ensure_ascii=False, indent=4)
            file_.write(str(data_))
