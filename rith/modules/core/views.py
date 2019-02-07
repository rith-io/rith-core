"""Core Module Package.

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


from flask import jsonify
from flask import redirect


from rith import oauth


from . import module


@module.route('/', methods=['GET'])
def core_redirect_options():
    """Define default index page redirect."""
    return redirect('/v1', 302)


@module.route('/v1', methods=['OPTIONS'])
def core_index_options():
    """Define default index page preflight check."""
    return jsonify(**{
        'meta': {
            'status': 200
        }
    })


@module.route('/v1', methods=['GET'])
def core_index_get():
    """Define default index page content."""
    return jsonify(**{
        'meta': {
            'status': 200
        },
        'properties': {
            'message': 'Welcome to the Arithmetic Framework, for information'
                       ' on using this application or to begin using this'
                       ' application in your organization contact'
                       ' support@rith.io.'
        }
    })
