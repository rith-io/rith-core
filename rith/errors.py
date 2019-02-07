"""Arithmetic ErrorHandlers for Built-in Flask errors.

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


from . import logger
from . import responses


from werkzeug.exceptions import BadRequestKeyError


from sqlalchemy.exc import ProgrammingError


from psycopg2 import IntegrityError


from oauthlib.oauth2 import TokenExpiredError
from oauthlib.oauth2 import InsecureTransportError
from oauthlib.oauth2 import MismatchingStateError
from oauthlib.oauth2 import MissingCodeError
from oauthlib.oauth2 import MissingTokenError
from oauthlib.oauth2 import MissingTokenTypeError
from oauthlib.oauth2 import FatalClientError
from oauthlib.oauth2 import InvalidRedirectURIError
from oauthlib.oauth2 import MissingRedirectURIError
from oauthlib.oauth2 import MismatchingRedirectURIError
from oauthlib.oauth2 import MissingClientIdError
from oauthlib.oauth2 import InvalidClientIdError
from oauthlib.oauth2 import InvalidRequestError
from oauthlib.oauth2 import AccessDeniedError
from oauthlib.oauth2 import UnsupportedResponseTypeError
from oauthlib.oauth2 import InvalidScopeError
from oauthlib.oauth2 import ServerError
from oauthlib.oauth2 import TemporarilyUnavailableError
from oauthlib.oauth2 import InvalidClientError
from oauthlib.oauth2 import InvalidGrantError
from oauthlib.oauth2 import UnauthorizedClientError
from oauthlib.oauth2 import UnsupportedGrantTypeError
from oauthlib.oauth2 import UnsupportedTokenTypeError


class ErrorHandlers(object):
    """Error handling for this Flask Application.

    :param object object: For a full explanation please see
    https://docs.python.org/release/2.2.3/whatsnew/sect-rellinks.html

    See the official Flask API documnetation for more information
    http://flask.pocoo.org/docs/0.10/patterns/errorpages/#error-handlers
    """

    def __init__(self, app):
        """Initialize all top level variables."""
        self.app = app

    def __repr__(self):
        """Display of ErrorHandler when inspected."""
        return '<ErrorHandler Viable Data>'

    def find_message(self, error):
        """Verify that error block has description.

        If no error.description exists then we need to return an empty string

        :param object error: The error object we wish to inspect

        :return string message: The message string produced by method
        """
        message = ''

        if hasattr(error, 'description'):
            message = error.description

        return message

    def load_errorhandler(self, app):
        """Define error handling responses for the application.

        See the official Flask API documentation for more information
        http://flask.pocoo.org/docs/0.10/api/#flask.Flask.errorhandler
        """
        @app.errorhandler(400)
        # @app.errorhandler(Exception)
        @app.errorhandler(BadRequestKeyError)
        @app.errorhandler(ProgrammingError)
        @app.errorhandler(IntegrityError)
        def internal_error(error):
            logger.error('ErrorHandler Exception %s', error)

            message = self.find_message(error)
            # if sentry:
            #     sentry.captureException()

            return responses.status_400(message), 400

        @app.errorhandler(401)
        # @app.errorhandler(Exception)
        def internal_error(error):
            logger.error('ErrorHandler Exception %s', error)

            message = self.find_message(error)
            # if sentry:
            #     sentry.captureException()

            return responses.status_401(message), 401

        @app.errorhandler(403)
        # @app.errorhandler(Exception)
        def internal_error(error):
            logger.error('ErrorHandler Exception %s', error)

            message = self.find_message(error)
            # if sentry:
            #     sentry.captureException()

            return responses.status_403(message), 403

        @app.errorhandler(404)
        def internal_error(error):
            logger.error('ErrorHandler Exception %s', error)

            message = self.find_message(error)
            # if sentry:
            #     sentry.captureException()

            return responses.status_404(message), 404

        @app.errorhandler(405)
        def internal_error(error):
            logger.error('ErrorHandler Exception %s', error)

            message = self.find_message(error)
            # if sentry:
            #     sentry.captureException()

            return responses.status_405(message), 405

        @app.errorhandler(410)
        def internal_error(error):
            logger.error('ErrorHandler Exception %s', error)

            message = self.find_message(error)
            # if sentry:
            #     sentry.captureException()

            return responses.status_410(message), 410

        @app.errorhandler(500)
        def internal_error(error):
            logger.error('ErrorHandler Exception %s', error)

            message = self.find_message(error)
            # if sentry:
            #     sentry.captureException()

            return responses.status_500(message), 500

        @app.errorhandler(TokenExpiredError)
        @app.errorhandler(InsecureTransportError)
        @app.errorhandler(MismatchingStateError)
        @app.errorhandler(MissingCodeError)
        @app.errorhandler(MissingTokenError)
        @app.errorhandler(MissingTokenTypeError)
        @app.errorhandler(FatalClientError)
        @app.errorhandler(InvalidRedirectURIError)
        @app.errorhandler(MissingRedirectURIError)
        @app.errorhandler(MismatchingRedirectURIError)
        @app.errorhandler(MissingClientIdError)
        @app.errorhandler(InvalidClientIdError)
        @app.errorhandler(InvalidRequestError)
        @app.errorhandler(AccessDeniedError)
        @app.errorhandler(UnsupportedResponseTypeError)
        @app.errorhandler(InvalidScopeError)
        @app.errorhandler(ServerError)
        @app.errorhandler(TemporarilyUnavailableError)
        @app.errorhandler(InvalidClientError)
        @app.errorhandler(InvalidGrantError)
        @app.errorhandler(UnauthorizedClientError)
        @app.errorhandler(UnsupportedGrantTypeError)
        @app.errorhandler(UnsupportedTokenTypeError)
        def internal_error(error):
            logger.error('OAuth Exception %s', error)

            message = self.find_message(error)
            # if sentry:
            #     sentry.captureException()

            return responses.status_500(message), 500
