"""Arithmetic Reusable Permission Methods.

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


from rith import logger
from rith import oauth


@oauth.require_oauth()
def verify_authorization(oauth_request, **kw):
    """Verify user has appropriate clearances to access data.

    :param object oauth_request: User object submitted through OAuth handlers

    :return object user: Return the user object or abort
    """
    if oauth_request.user:
        logger.info('User %d requesting system authorization' %
                    oauth_request.user.id)
        if not oauth_request.user.active:
            logger.warning('User %d is inactive and is requesting access to'
                           'system resources.' % (oauth_request.user.id))

            abort(401)
        return oauth_request.user

    #
    # @todo add ip address, access token used, and any other information that
    # would be used in blocking or singling out offending user accounts
    #
    logger.warning('An invalid access_token was submitted')
    abort(403)


def verify_roles(user_object, role_required):
    """Verify the user has a required system role.

    :param object user_object: The user object to check for roles
    :param string role_required: The role that is required to access resource
    """
    if not check_roles(role_required, user_object.roles):
        logger.warning('User %d attempted to access a protected resource '
                       'without the appropriate %s role' %
                       (user_object.id, role_required))
        abort(403)


def check_roles(role_required, role_list):
    """Verify string is within the list.

    :param string role_required: The string to find
    :param list role_list: The list of user roles

    :return boolean: True or False based on whether string was found
    """
    for index, role in enumerate(role_list):
        if role.name in role_required:
            return True

    return False
