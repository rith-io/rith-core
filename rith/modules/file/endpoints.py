"""Arithmetic File Module.

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


from datetime import datetime


from flask import abort
from flask import json
from flask import request


from rith import logger
from rith.endpoint import Endpoint
from rith.permissions import *


class Seed(Endpoint):
    """Instantiate the File Endpoints.

    :param class Endpoint: The Endpoint base class

    See the official Flask Restless documentation for more information
    https://flask-restless.readthedocs.org/en/latest/
    """

    """Define all base preprocessors.

    See the official Flask Restless documentation for more information
    https://flask-restless.readthedocs.org/en/latest/customizing.html\
    #request-preprocessors-and-postprocessors
    """

    def file_preprocessor_get_single(instance_id=None, **kw):
        """Create an File specific GET_SINGLE preprocessor.

        Accepts a single argument, `instance_id`, the primary key of the
        instance of the model to get.
        """
        logger.info('`file_preprocessor_get_single` responded to request')

        if request.args.get('access_token', '') or \
                request.headers.get('Authorization'):

            authorization = verify_authorization()

        else:
            abort(403)

    def file_preprocessor_get_many(search_params=None, **kw):
        """Create an File specific GET_MANY preprocessor.

        Accepts a single argument, `search_params`, which is a dictionary
        containing the search parameters for the request.
        """
        logger.info('`file_preprocessor_get_many` responded to request')

        if request.args.get('access_token', '') or \
                request.headers.get('Authorization'):

            authorization = verify_authorization()

        else:
            abort(403)

    def file_preprocessor_update_single(instance_id=None, **kw):
        """Create an File specific PATCH_SINGLE and PUT_SINGLE preprocessor.

        Accepts two arguments, `instance_id`, the primary key of the
        instance of the model to patch, and `data`, the dictionary of fields
        to change on the instance.
        """
        logger.info('`file_preprocessor_update_single` used for endpoint')

        if request.args.get('access_token', '') or \
                request.headers.get('Authorization'):

            authorization = verify_authorization()

        else:
            abort(403)

    def file_preprocessor_update_many(search_params=None, **kw):
        """Create an File specific PATCH_MANY and PATCH_SINGLE preprocessor.

        Accepts two arguments: `search_params`, which is a dictionary
        containing the search parameters for the request, and `data`, which
        is a dictionary representing the fields to change on the matching
        instances and the values to which they will be set.
        """
        logger.info('`file_preprocessor_update_many` used for endpoint')

        if request.args.get('access_token', '') or \
                request.headers.get('Authorization'):

            authorization = verify_authorization()

            data['modified_on'] = datetime.now().isoformat()
            data['last_modified_by_id'] = authorization.id

        else:
            abort(403)

    def file_preprocessor_post(data=None, **kw):
        """Create an File specific POST preprocessor.

        Accepts a single argument, `data`, which is the dictionary of
        fields to set on the new instance of the model.
        """
        logger.info('`file_preprocessor_post` used for endpoint')

        if request.args.get('access_token', '') or \
                request.headers.get('Authorization'):

            authorization = verify_authorization()

            data['created_on'] = datetime.now().isoformat()
            data['modified_on'] = datetime.now().isoformat()

            data['creator_id'] = authorization.id
            data['last_modified_by_id'] = authorization.id

        else:
            abort(403)

    def file_preprocessor_delete_single(instance_id=None, **kw):
        """Create an File specific DELETE_SINGLE preprocessor.

        Accepts a single argument, `instance_id`, which is the primary key
        of the instance which will be deleted.
        """
        logger.info('`file_preprocessor_delete_single` used for endpoint')

        if request.args.get('access_token', '') or \
                request.headers.get('Authorization'):

            authorization = verify_authorization()

        else:
            abort(403)

    """Define all base postprocessors.

    See the official Flask Restless documentation for more information
    https://flask-restless.readthedocs.org/en/latest/customizing.html\
    #request-preprocessors-and-postprocessors
    """

    def file_postprocessor_get_single(result=None, **kw):
        """Create an File specific GET_SINGLE postprocessor.

        Accepts a single argument, `result`, which is the dictionary
        representation of the requested instance of the model.
        """
        logger.info('`file_postprocessor_get_single` responded to request')

    def file_postprocessor_get_many(result=None, search_params=None, **kw):
        """Create an File specific GET_MANY postprocessor.

        Accepts two arguments, `result`, which is the dictionary
        representation of the JSON response which will be returned to the
        client, and `search_params`, which is a dictionary containing the
        search parameters for the request (that produced the specified
        `result`).
        """
        logger.info('`file_postprocessor_get_many` responded to request')

    def file_postprocessor_update_single(result=None, **kw):
        """Create an File specific PATCH_SINGLE and PUT_SINGLE postprocessor.

        Accepts a single argument, `result`, which is the dictionary
        representation of the requested instance of the model.
        """
        logger.info('`file_postprocessor_update_single` used for endpoint')

    def file_postprocessor_update_many(query=None, data=None,
                                       search_params=None, **kw):
        """Create an File specific PATCH_MANY and PATCH_SINGLE postprocessor.

        Accepts three arguments: `query`, which is the SQLAlchemy query
        which was inferred from the search parameters in the query string,
        `data`, which is the dictionary representation of the JSON response
        which will be returned to the client, and `search_params`, which is a
        dictionary containing the search parameters for the request.
        """
        logger.info('`file_postprocessor_update_many` used for endpoint')

    def file_postprocessor_post(result=None, **kw):
        """Create an File specific POST postprocessor.

        Accepts a single argument, `result`, which is the dictionary
        representation of the created instance of the model.
        """
        logger.info('`file_postprocessor_post` used for endpoint')

    def file_postprocessor_delete_single(was_deleted=None, **kw):
        """Create an File specific DELETE_SINGLE postprocessor.

        Accepts a single argument, `was_deleted`, which represents whether
        the instance has been deleted.
        """
        logger.info('`file_postprocessor_delete_single` used for endpoint')

    def file_postprocessor_delete_many(result=None, search_params=None,
                                       **kw):
        """Create an File specific DELETE_MANY postprocessor.

        Accepts two arguments: `result`, which is the dictionary
        representation of which is the dictionary representation of the JSON
        response which will be returned to the client, and `search_params`,
        which is a dictionary containing the search parameters for the
        request.
        """
        logger.info('`file_postprocessor_delete_many` used for endpoint')

    """Flask-Restless Endpoint Arguments.

    These arguments define how the endpoint will be setup. These are the
    defaults that we will use. These arguments can be overridden once a new
    Endpoint class has been instantiated.

    See the official Flask-Restless documentation for more information
    https://flask-restless.readthedocs.org/en/latest/api.html#\
    flask.ext.restless.APIManager.create_api_blueprint
    """
    __arguments__ = {
        'collection_name': 'file',
        'url_prefix': '/v1/data',
        'exclude_columns': [],
        'max_results_per_page': 25,
        'methods': [
            'GET',
            'POST',
            'PATCH',
            'PUT',
            'DELETE'
        ],
        'preprocessors': {
            'GET_SINGLE': [file_preprocessor_get_single],
            'GET_MANY': [file_preprocessor_get_many],
            'PATCH_SINGLE': [file_preprocessor_update_single],
            'POST': [file_preprocessor_post],
            'DELETE': [file_preprocessor_delete_single]
        },
        'postprocessors': {
            'GET_SINGLE': [file_postprocessor_get_single],
            'GET_MANY': [file_postprocessor_get_many],
            'PATCH_SINGLE': [file_postprocessor_update_single],
            'POST': [file_postprocessor_post],
            'DELETE': [file_postprocessor_delete_single]
        },
        'allow_functions': False,
        'allow_delete_many': False,
        'allow_patch_many': False
    }
