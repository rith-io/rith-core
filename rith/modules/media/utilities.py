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


import sys
import os.path


from uuid import uuid4
from werkzeug import secure_filename
from wand.image import Image


from flask import current_app


from rith import logger


def allowed_file(filename):
    """Ensure file upload being attempted is of an allowed file type."""
    logger.debug('Checking if file name is valid')

    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def thumbnail(image, width=1280, height=1280):
    """Create a square thumbnail based on an image, a width, and height."""
    logger.debug('Thumbnail creation started')

    dst_landscape = 1 > image.width / image.height

    wh = image.width if dst_landscape else image.height

    image.crop(
        left=int((image.width - wh) / 2),
        top=int((image.height - wh) / 2),
        width=int(wh),
        height=int(wh)
    )

    image.resize(width, height)
    logger.debug('[MEDIA utilities:thumbnail] Thumbnail creation completed')


def create(image, name, suffix, extension, directory, size={}):
    """Create an image according to spec."""
    logger.debug('[MEDIA utilities:create] Image creation process started')

    filename = name + suffix + extension
    filepath = os.path.join(directory, 'images', filename)

    with image.clone() as temporary_image:

        if 'width' in size and 'height' in size:
            thumbnail(temporary_image, size.get('width'), size.get('height'))

        temporary_image.save(filename=filepath)

    logger.debug('Image creation completed with file:`%s`' % (filename))
    return filename


def upload_image(source_file, acl='public-read'):
    """Upload File Object."""
    logger.debug('[MEDIA utilities:upload_image] Image upload process started')

    basepath = current_app.config['MEDIA_BASE_PATH'] + 'images/'
    directory = current_app.config['MEDIA_DIRECTORY']

    """
    Prepare the file for processing
    """
    source_filename = secure_filename(source_file.filename)
    source_extension = os.path.splitext(source_filename)[1]

    destination_filename = uuid4().hex

    try:
        image = Image(file=source_file)
        image.format = 'jpeg'
        image.compression_quality = 75
        logger.debug('Completed creating image object `%s`' % (image))
    except Exception:
        logger.debug('Couldn\'t create transformable image object')
        raise

    try:
        """
        Fix EXIF Orientation
        """
        _orientation = image.metadata.get('exif:Orientation')

        if _orientation == '1':
            pass
        elif _orientation == '2':
            image.flop()
        elif _orientation == '3':
            image.rotate(180)
        elif _orientation == '4':
            image.flop()
            image.rotate(180)
        elif _orientation == '5':
            image.flip()
            image.rotate(90)
        elif _orientation == '6':
            image.rotate(90)
        elif _orientation == '7':
            image.flip()
            image.rotate(270)
        elif _orientation == '8':
            image.rotate(270)

        """
        ORIGINAL:
        """
        original_filename = create(**{
            'image': image,
            'name': destination_filename,
            'suffix': '_original',
            'extension': source_extension,
            'directory': directory
        })

        logger.debug('Completed rotating original orientation')
    except Exception:
        logger.debug('Exception raised trying to rotate original orientation')
        raise

    try:
        """
        SQUARE: We save this at @2x of 640px (1280px)
        """
        square_retina_filename = create(**{
            'image': image,
            'name': destination_filename,
            'suffix': '_square@2x',
            'extension': source_extension,
            'size': {
                'width': 1280,
                'height': 1280
            },
            'directory': directory
        })

        square_filename = create(**{
            'image': image,
            'name': destination_filename,
            'suffix': '_square',
            'extension': source_extension,
            'size': {
                'width': 640,
                'height': 640
            },
            'directory': directory
        })

        """
        THUMBNAIL: We save this at @2x of 256px (512px)
        """
        thumbnail_retina_filename = create(**{
            'image': image,
            'name': destination_filename,
            'suffix': '_thumbnail@2x',
            'extension': source_extension,
            'size': {
                'width': 512,
                'height': 512
            },
            'directory': directory
        })

        thumbnail_filename = create(**{
            'image': image,
            'name': destination_filename,
            'suffix': '_thumbnail',
            'extension': source_extension,
            'size': {
                'width': 256,
                'height': 256
            },
            'directory': directory
        })

        """
        Icon: We save this at @2x of 64px (128px)
        """
        icon_retina_filename = create(**{
            'image': image,
            'name': destination_filename,
            'suffix': '_icon@2x',
            'extension': source_extension,
            'size': {
                'width': 128,
                'height': 128
            },
            'directory': directory
        })

        icon_filename = create(**{
            'image': image,
            'name': destination_filename,
            'suffix': '_icon',
            'extension': source_extension,
            'size': {
                'width': 64,
                'height': 64
            },
            'directory': directory
        })

        logger.debug('Image upload process complete')
        return {
            'original': os.path.join(basepath, original_filename),
            'square': os.path.join(basepath, square_filename),
            'square_retina': os.path.join(basepath, square_retina_filename),
            'thumbnail': os.path.join(basepath, thumbnail_filename),
            'thumbnail_retina': os.path.join(basepath,
                                             thumbnail_retina_filename),
            'icon': os.path.join(basepath, icon_filename),
            'icon_retina': os.path.join(basepath, icon_retina_filename)
        }
    except Exception:
        logger.debug('Exception raised trying to create multiple formats')
        raise


def upload_file(source_file, acl='public-read'):
    """Upload a File Object Directly to our server."""
    logger.debug('[MEDIA utilities:upload_file] File upload process started')

    basepath = current_app.config['MEDIA_BASE_PATH']
    directory = current_app.config['MEDIA_DIRECTORY']

    """
    Prepare the file for processing
    """
    extension = os.path.splitext(source_file.filename)[1]
    secure_filename = uuid4().hex + extension

    filepath = os.path.join(directory, secure_filename)
    fileurl = os.path.join(basepath, secure_filename)

    try:
        logger.debug('Saving file source information to server')
        source_file.save(filepath)
    except Exception:
        logger.debug('Exception raised saving file source to server')
        raise

    logger.debug('File upload process completed with original:%s' % (fileurl))
    return {
        'original': fileurl
    }
