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
from flask import json
from flask import jsonify
from flask import request


from rith import db
from rith import oauth


from . import Model
from . import module


@module.route('/v1/data/user/me', methods=['OPTIONS'])
def user_me_options():
    """Define default user preflight check."""
    return jsonify(**{
        'meta': {
            'status': 200
        }
    })


@module.route('/v1/data/user/me', methods=['GET'])
@oauth.require_oauth()
def user_me_get(oauth_request):
    """Define default user request."""
    _user = oauth_request.user

    if not hasattr(_user, 'id'):
        abort(403)

    return jsonify(**_user.user_get()), 200
