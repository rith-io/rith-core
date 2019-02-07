"""Arithmetic OAuth Module.

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
from datetime import timedelta


from flask import abort
from flask import after_this_request
from flask import current_app
from flask import jsonify
from flask import request
from flask import render_template
from flask import url_for


from flask_security import current_user
from flask_security import login_required
from flask_security import login_user


from werkzeug.datastructures import MultiDict
from werkzeug.local import LocalProxy
from werkzeug.security import gen_salt


from rith import db
from rith import logger
from rith import oauth
from rith import responses
from rith.schema.client import Client
from rith.schema.grant import Grant
from rith.schema.token import Token


from . import module


"""Load the Security extension and access the datastore."""
_security = LocalProxy(lambda: current_app.extensions['security'])
_datastore = LocalProxy(lambda: _security.datastore)


"""OAuth Implementation for system access

See the official Flask OAuthlib documentation for more information
https://flask-oauthlib.readthedocs.org/en/latest/
"""


@module.route('/v1/auth/client')
@login_required
def oauth_client():
    """Generate a Client object to create apps with."""
    next_url = url_for('oauth.oauth_client', **request.args)

    """
    If the user is not authenticated we should redirect them
    to the login page
    """
    if not hasattr(current_user, 'id'):
        return redirect(url_for('security.login', next=next_url))

    """
    Assign the current_user object to a variable so that we don't
    accidently alter the object during this process.
    """
    this_user = current_user

    """
    Generate a client_id and client_secret for our OAuth2 authentication
    """
    client_id = gen_salt(40)
    client_secret = gen_salt(50)
    _redirect_uris = 'http://127.0.0.1:9000/authorize'
    _default_scopes = 'user'
    user_id = this_user.id

    item = Client(
        client_id=client_id,
        client_secret=client_secret,
        _redirect_uris=_redirect_uris,
        _default_scopes=_default_scopes,
        user_id=user_id,
     )

    """Save the OAuth2 authentication information to the database."""
    db.session.add(item)
    db.session.commit()

    return jsonify(**{
        'client_key': client_id,
        'client_secret': client_secret
    }), 200


@module.route('/v1/auth/token')
@oauth.token_handler
def access_token():
    """Token Handler."""
    return None


@module.route('/v1/auth/authorize', methods=['GET', 'POST'])
@login_required
@oauth.authorize_handler
def authorize(*args, **kwargs):
    """Handle for authorization of login information."""
    next_url = url_for('oauth.authorize', **{
        'response_type': request.args.get('response_type'),
        'client_id': request.args.get('client_id'),
        'redirect_uri': request.args.get('redirect_uri'),
        'scope': request.args.get('scope')
    })

    if not hasattr(current_user, 'id'):
        return redirect(url_for('security.login', next=next_url))

    """
    Assign the current_user object to a variable so that we don't
    accidently alter the object during this process.
    """
    this_user = current_user

    if request.method == 'GET':
        client_id = kwargs.get('client_id')
        client = Client.query.filter_by(client_id=client_id).first()
        kwargs['client'] = client
        kwargs['user'] = this_user
        return render_template('oauth/authorize.html', **kwargs)

    confirm = request.form.get('confirm', 'no')

    return confirm == 'yes'


@module.route('/v1/auth/remote/login', methods=['POST'])
@oauth.authorize_handler
def remote_authorize(*args, **kwargs):
    """Login via JSON from another application.

    :param string email: Email associated with user account
    :param string password: Password assocaited with user account

    :return bool
    """
    form_class = _security.login_form

    error_message = 'No credentials provided'

    if request.json:
        form = form_class(MultiDict(request.json))
    else:
        error_message = "Request did not use Content-Type:application/json"
        logger.info('[OAUTH::remote_authorize] %s', error_message)
        abort(403, error_message)

    if form.validate_on_submit():
        login_user(form.user, remember=form.remember.data)
        after_this_request(_commit)

        current_user = form.user
    else:
        logger.error('[OAUTH::remote_authorize] Validation Failed with '
                     'message: %s', form.errors)
        return abort(403, form.errors)

    return True


@module.route('/v1/auth/logout', methods=['POST'])
@oauth.require_oauth()
def remote_logout(oauth_request, *args, **kwargs):
    """Logout via JSON from another application."""
    if not oauth_request.access_token:
        abort(403)

    db.session.delete(oauth_request.access_token)
    db.session.commit()

    return jsonify(**{
        'meta': {
            'status': 200
        }
    }), 200


@oauth.clientgetter
def load_client(client_id):
    r"""Determine which client is sending the request.

    See the official Flask OAuthlib documentation for more information
    https://flask-oauthlib.readthedocs.org/en/latest/oauth2.html\
    #client-getter
    """
    return Client.query.filter_by(client_id=client_id).first()


@oauth.grantgetter
def load_grant(client_id, code):
    r"""Assist in the authorization workflow.

    See the official Flask OAuthlib documentation for more information
    https://flask-oauthlib.readthedocs.org/en/latest/oauth2.html\
    #client-getter
    """
    return Grant.query.filter_by(client_id=client_id, code=code).first()


@oauth.grantsetter
def save_grant(client_id, code, request, *args, **kwargs):
    r"""Assist in the authorization workflow.

    See the official Flask OAuthlib documentation for more information
    https://flask-oauthlib.readthedocs.org/en/latest/oauth2.html\
    #client-getter
    """
    expires = datetime.utcnow() + timedelta(days=1)
    grant = Grant(
        client_id=client_id,
        code=code['code'],
        redirect_uri=request.redirect_uri,
        _scopes=' '.join(request.scopes),
        user=current_user,
        expires=expires
    )
    db.session.add(grant)
    db.session.commit()
    return grant


@oauth.tokengetter
def load_token(access_token=None, refresh_token=None):
    r"""Assist in the authorization workflow.

    See the official Flask OAuthlib documentation for more information
    https://flask-oauthlib.readthedocs.org/en/latest/oauth2.html\
    #token-getter-and-setter
    """
    if access_token:
        return Token.query.filter_by(access_token=access_token).first()
    elif refresh_token:
        return Token.query.filter_by(refresh_token=refresh_token).first()


@oauth.tokensetter
def save_token(token, oauth_request, *args, **kwargs):
    r"""Assist in the authorization workflow.

    See the official Flask OAuthlib documentation for more information
    https://flask-oauthlib.readthedocs.org/en/latest/oauth2.html\
    #token-getter-and-setter
    """
    if current_user.is_anonymous:
        abort(403, 'The email or password you provided was incorrect')

    toks = Token.query.filter_by(
        client_id=oauth_request.client.client_id,
        user_id=current_user.id
    )

    expires = datetime.utcnow() + timedelta(days=1)

    tok = Token(
        access_token=token['access_token'],
        # refresh_token=token['refresh_token'],
        token_type=token['token_type'],
        _scopes=token['scope'],
        expires=expires,
        client_id=oauth_request.client.client_id,
        user_id=current_user.id
    )
    db.session.add(tok)
    db.session.commit()

    return tok


def _commit(response=None):
    """Commit to the security datastore."""
    _datastore.commit()

    return response
