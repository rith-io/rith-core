"""Arithmetic User Module.

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


from flask import abort
from flask import request


from rith import db
from rith import logger


from rith.endpoint import Endpoint


from rith.permissions import *


from . import Model


from flask_security.utils import send_mail
from flask_security.utils import config_value
from flask_security.utils import url_for_security


from flask_security.recoverable import generate_reset_password_token


class Seed(Endpoint):
    """Instantiate the User Endpoints.

    :param class Endpoint: The Endpoint base class

    See the official Flask Restless documentation for more information
    https://flask-restless.readthedocs.org/en/latest/
    """

    """Define all base preprocessors.

    See the official Flask Restless documentation for more information
    https://flask-restless.readthedocs.org/en/latest/customizing.html\
    #request-preprocessors-and-postprocessors
    """

    def user_preprocessor_get_single(instance_id=None, **kw):
        """Create an User specific GET_SINGLE preprocessor.

        Accepts a single argument, `instance_id`, the primary key of the
        instance of the model to get.
        """
        logger.info('`user_preprocessor_get_single` responded to request')

        if request.args.get('access_token', '') or \
                request.headers.get('Authorization'):

            authorization = verify_authorization()

            if check_roles('generic', authorization.roles):
                logger.warning('User %d %s access failed User GET_SINGLE' %
                               (authorization.id, 'grantee'))
                logger.warning('generic role unauthorized to access '
                               'User GET_SINGLE')
                pass
            else:
                logger.info('User %d accessed User GET_SINGLE with no'
                            'role' %
                            (authorization.id))
                abort(403)
        else:
            logger.info('Anonymous user attempted to access User'
                        'GET_SINGLE')
            abort(403)

    def user_preprocessor_get_many(search_params=None, **kw):
        """Create an User specific GET_MANY preprocessor.

        Accepts a single argument, `search_params`, which is a dictionary
        containing the search parameters for the request.
        """
        logger.info('`user_preprocessor_get_many` responded to request')

        if request.args.get('access_token', '') or \
                request.headers.get('Authorization'):

            authorization = verify_authorization()

            if check_roles('generic', authorization.roles):
                logger.warning('User %d %s access failed User GET_MANY' %
                               (authorization.id, 'generic'))
                logger.warning('generic role unauthorized to access '
                               'User GET_MANY')
                pass
            else:
                logger.info('User %d accessed User GET_MANY with no role' %
                            (authorization.id))
                abort(403)
        else:
            logger.info('Anonymous user attempted to access User GET_MANY')
            abort(403)

    def user_preprocessor_update_single(instance_id=None, **kw):
        """Create an User specific PATCH_SINGLE and PUT_SINGLE preprocessor.

        Accepts two arguments, `instance_id`, the primary key of the
        instance of the model to patch, and `data`, the dictionary of fields
        to change on the instance.
        """
        logger.info('`user_preprocessor_update_single` used for endpoint')

        if request.args.get('access_token', '') or \
                request.headers.get('Authorization'):

            authorization = verify_authorization()
            if (int(authorization.id) == int(instance_id)):
                logger.debug('User %d updating their account' %
                             (authorization.id))

                pass
            elif check_roles('admin', authorization.roles):
                logger.info('Administrator with id %d is updating user id %d' %
                            (authorization.id, int(instance_id)))
                pass
            else:
                logger.info('User %d attempted to access a User UPDATE_SINGLE '
                            'for another user account' %
                            (authorization.id))
                abort(403)
        else:
            logger.info('Anonymous user attempted to access User'
                        'UPDATE_SINGLE')
            abort(403)

    def user_preprocessor_update_many(search_params=None, **kw):
        """Create an User specific PATCH_MANY and PATCH_SINGLE preprocessor.

        Accepts two arguments: `search_params`, which is a dictionary
        containing the search parameters for the request, and `data`, which
        is a dictionary representing the fields to change on the matching
        instances and the values to which they will be set.
        """
        logger.info('`user_preprocessor_update_many` used for endpoint')

        if request.args.get('access_token', '') or \
                request.headers.get('Authorization'):

            authorization = verify_authorization()

            if check_roles('generic', authorization.roles):
                logger.warning('User %d %s access failed User '
                               'UPDATE_MANY' %
                               (authorization.id, 'generic'))
                logger.warning('generic role unauthorized to access '
                               'User UPDATE_MANY')
                abort(401)
            else:
                logger.info('User %d accessed User UPDATE_MANY '
                            'with no role' %
                            (authorization.id))
                abort(403)
        else:
            logger.info('Anonymous user attempted to access User'
                        'UPDATE_MANY')
            abort(403)

    def user_preprocessor_post(data=None, **kw):
        """Create an User specific POST preprocessor.

        Accepts a single argument, `data`, which is the dictionary of
        fields to set on the new instance of the model.
        """
        logger.info('`user_preprocessor_post` used for endpoint')

        if request.args.get('access_token', '') or \
                request.headers.get('Authorization'):

            authorization = verify_authorization()

            if check_roles('generic', authorization.roles) and \
               not check_roles('admin', authorization.roles):
                logger.warning('User %d %s access failed User POST' %
                               (authorization.id, 'generic'))
                logger.warning('generic role unauthorized to access '
                               'User POST')
                abort(401)
            elif check_roles('admin', authorization.roles):
                logger.info('User %d accessed User POST as %s' %
                            (authorization.id, 'admin'))
                pass
            else:
                logger.info('User %d accessed User POST with no role' %
                            (authorization.id))
                abort(403)
        else:
            logger.info('Anonymous user attempted to access User POST')
            abort(403)

    def user_preprocessor_delete_single(instance_id=None, **kw):
        """Create an User specific DELETE_SINGLE preprocessor.

        Accepts a single argument, `instance_id`, which is the primary key
        of the instance which will be deleted.
        """
        logger.info('`user_preprocessor_delete_single` used for endpoint')

        if request.args.get('access_token', '') or \
                request.headers.get('Authorization'):

            authorization = verify_authorization()

            if check_roles('generic', authorization.roles) and\
               not check_roles('admin', authorization.roles):
                logger.warning('User %d %s access failed User '
                               'DELETE_SINGLE' %
                               (authorization.id, 'generic'))
                logger.warning('generic role unauthorized to access '
                               'User DELETE_SINGLE')
                abort(401)
            elif check_roles('admin', authorization.roles):
                pass
            else:
                logger.info('User %d accessed User DELETE_SINGLE with '
                            'no role' %
                            (authorization.id))
                abort(403)
        else:
            logger.info('Anonymous user attempted to access User '
                        'DELETE_SINGLE')
            abort(403)

    """Define all base postprocessors.

    See the official Flask Restless documentation for more information
    https://flask-restless.readthedocs.org/en/latest/customizing.html\
    #request-preprocessors-and-postprocessors
    """

    def user_postprocessor_get_single(result=None, **kw):
        """Create an User specific GET_SINGLE postprocessor.

        Accepts a single argument, `result`, which is the dictionary
        representation of the requested instance of the model.
        """
        logger.info('`user_postprocessor_get_single` responded to request')

    def user_postprocessor_get_many(result=None, search_params=None, **kw):
        """Create an User specific GET_MANY postprocessor.

        Accepts two arguments, `result`, which is the dictionary
        representation of the JSON response which will be returned to the
        client, and `search_params`, which is a dictionary containing the
        search parameters for the request (that produced the specified
        `result`).
        """
        logger.info('`user_postprocessor_get_many` responded to request')

    def user_postprocessor_update_single(result=None, **kw):
        """Create an User specific PATCH_SINGLE and PUT_SINGLE postprocessor.

        Accepts a single argument, `result`, which is the dictionary
        representation of the requested instance of the model.
        """
        logger.info('`user_postprocessor_update_single` used for endpoint')

    def user_postprocessor_update_many(query=None, data=None,
                                       search_params=None, **kw):
        """Create an User specific PATCH_MANY and PATCH_SINGLE postprocessor.

        Accepts three arguments: `query`, which is the SQLAlchemy query
        which was inferred from the search parameters in the query string,
        `data`, which is the dictionary representation of the JSON response
        which will be returned to the client, and `search_params`, which is a
        dictionary containing the search parameters for the request.
        """
        logger.info('`user_postprocessor_update_many` used for endpoint')

    def user_postprocessor_post(result=None, **kw):
        """Create an User specific POST postprocessor.

        Accepts a single argument, `result`, which is the dictionary
        representation of the created instance of the model.
        """
        logger.info('`user_postprocessor_post` used for endpoint')

        authorization = verify_authorization()
        role = verify_roles(authorization, ['admin'])

        """
        HACK: We really shouldn't be doing this, however, it's quicker and
              more straight forward than converting the <dict> to enable
              dot sytnax that is compatible with Flask-Security

        """
        user = db.session.query(Model).get(result['id'])

        """
        Sends the reset password instructions email for the specified user.

        :param user: The user to send the instructions to

        """
        token = generate_reset_password_token(user)
        reset_link = url_for_security('reset_password', token=token,
                                      _external=True)

        send_mail('An administrator has created an account for you',
                  user.email, 'staff', user=user, confirmation_link=reset_link)

    def user_postprocessor_delete_single(was_deleted=None, **kw):
        """Create an User specific DELETE_SINGLE postprocessor.

        Accepts a single argument, `was_deleted`, which represents whether
        the instance has been deleted.
        """
        logger.info('`user_postprocessor_delete_single` used for endpoint')

    def user_postprocessor_delete_many(result=None, search_params=None,
                                       **kw):
        """Create an User specific DELETE_MANY postprocessor.

        Accepts two arguments: `result`, which is the dictionary
        representation of which is the dictionary representation of the JSON
        response which will be returned to the client, and `search_params`,
        which is a dictionary containing the search parameters for the
        request.
        """
        logger.info('`user_postprocessor_delete_many` used for endpoint')

    """Flask-Restless Endpoint Arguments.

    These arguments define how the endpoint will be setup. These are the
    defaults that we will use. These arguments can be overridden once a new
    Endpoint class has been instantiated.

    See the official Flask-Restless documentation for more information
    https://flask-restless.readthedocs.org/en/latest/api.html#\
    flask.ext.restless.APIManager.create_api_blueprint
    """
    __arguments__ = {
        'url_prefix': '/v1/data',
        'exclude_columns': [],
        'max_results_per_page': 500,
        'methods': [
            'GET',
            'POST',
            'PATCH',
            'PUT',
            'DELETE'
        ],
        'preprocessors': {
            'GET_SINGLE': [user_preprocessor_get_single],
            'GET_MANY': [user_preprocessor_get_many],
            'PUT_SINGLE': [user_preprocessor_update_single],
            'PUT_MANY': [user_preprocessor_update_many],
            'PATCH_SINGLE': [user_preprocessor_update_single],
            'PATCH_MANY': [user_preprocessor_update_many],
            'POST': [user_preprocessor_post],
            'DELETE': [user_preprocessor_delete_single]
        },
        'postprocessors': {
            'GET_SINGLE': [user_postprocessor_get_single],
            'GET_MANY': [user_postprocessor_get_many],
            'PUT_SINGLE': [user_postprocessor_update_single],
            'PUT_MANY': [user_postprocessor_update_many],
            'PATCH_SINGLE': [user_postprocessor_update_single],
            'PATCH_MANY': [user_postprocessor_update_many],
            'POST': [user_postprocessor_post],
            'DELETE': [user_postprocessor_delete_single]
        },
        'allow_functions': True,
        'allow_patch_many': False
    }
