"""Arithmetic Media Module.

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
from flask import current_app
from flask import jsonify
from flask import request
from flask import send_from_directory


from rith import db
from rith import logger
from rith import oauth


from . import module


from .utilities import upload_file
from .utilities import upload_image


from rith.schema.file import File
from rith.schema.image import Image


from rith.permissions import verify_authorization


@module.route('/v1/media/image', methods=['POST'])
@oauth.require_oauth()
def image_post(oauth_request):
    """Image Post."""
    logger.debug('Begin processing image processing request')

    """
    Check to see that one and only one file has been attached to this request
    before proceding with the file upload
    """
    if not len(request.files) or len(request.files) > 1:
        return abort(400, 'Please attach a single file to this request')

    """Check to see if there is an `image` attribute in the `request.files`."""
    if 'image' not in request.files:
        logger.debug('Missing `image` attribute in `request.files`')

    _file = request.files['image']
    logger.debug('request.files with value of `%s`' % (_file))

    """
    Upload the file to our server
    """
    output = upload_image(_file)

    if not output:
        logger.debug('Output from image processing return `None`')
        return jsonify(**{
            'code': 415,
            'status': 'Unsupported Media Type',
            'message': 'Unable to process image at the `upload_image` method'
        }), 415

    """
    Create and Save the new Media object
    """
    logger.debug('Ouput accepted as `%s`, save Image object' % (output))
    media = Image(**{
        'original': output['original'],
        'square': output['square'],
        'square_retina': output['square_retina'],
        'thumbnail': output['thumbnail'],
        'thumbnail_retina': output['thumbnail_retina'],
        'icon': output['icon'],
        'icon_retina': output['icon_retina'],
        'filename': _file.filename,
        'filetype': _file.mimetype,
        'filesize': _file.content_length,
        'created_on': datetime.now().isoformat(),
        'creator_id': oauth_request.user.id
    })
    logger.debug('Image object created successfully `%s`' % (media))

    db.session.add(media)
    db.session.commit()

    logger.debug('Image object committed to database')

    """
    Return the finalized Image resource
    """
    _return_value = {
        'id': media.id,
        'created_on': media.created_on,
        'modified_on': media.modified_on,
        'creator_id': media.creator_id,
        'original': media.original,
        'square': media.square,
        'square_retina': media.square_retina,
        'thumbnail': media.thumbnail,
        'thumbnail_retina': media.thumbnail_retina,
        'icon': media.icon,
        'icon_retina': media.icon_retina,
        'filename': media.filename,
        'filetype': media.filetype,
        'filesize': media.filesize,
        'caption': media.caption,
        'caption_link': media.caption_link
    }

    logger.debug('Completed processing image processing request')
    return jsonify(**_return_value), 200


@module.route('/v1/media/file', methods=['POST'])
@oauth.require_oauth()
def file_post(oauth_request):
    """FILE POST.

    Check to see that one and only one file has been attached to this request
    before proceding with the file upload
    """
    if not len(request.files) or len(request.files) > 1:
        return abort(400, 'Please attach a single file to this request')

    """
    Grab the file from the Request object
    """
    file = request.files['file']

    """
    Upload the file to Amazon S3
    """
    output = upload_file(file)

    """
    Create and Save the new File object
    """
    media = File(**{
        'creator_id': oauth_request.user.id,
        'filepath': output['original'],
        'filename': file.filename,
        'filetype': file.mimetype,
        'filesize': file.content_length,
        'created_on': datetime.now().isoformat()
    })

    db.session.add(media)
    db.session.commit()

    """
    Return the finalized Image resource
    """
    return jsonify(**{
        'id': media.id,
        'created_on': media.created_on,
        'modified_on': media.modified_on,
        'creator_id': media.creator_id,
        'filepath': media.filepath,
        'filename': media.filename,
        'filetype': media.filetype,
        'filesize': media.filesize
    }), 200
