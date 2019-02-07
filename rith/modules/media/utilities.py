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

"""
Import System Dependencies
"""
import pexif
import sys

import os.path

from uuid import uuid4

"""
Import Flask Dependencies
"""
from werkzeug import secure_filename

from flask import current_app

from wand.image import Image

from app import logger


"""
Make sure that the file upload being attempted is of an allowed file type
"""
def allowed_file(filename):
    logger.debug('[MEDIA utilities:allowed_file] Checking if file name is valid')
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


"""
Create a square thumbnail based on an image, a width, and height
"""
def thumbnail(image, width=1280, height=1280):

    logger.debug('[MEDIA utilities:thumbnail] Thumbnail creation started')
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


"""
Save the image with a new Exif Rotation
"""
def orientation(filepath, _new_orientation=1):

    logger.debug('[MEDIA utilities:orientation] Verifying orientation, JPEG files only, orientation to be set to `%s`' % (_new_orientation))

    """
    1. Open the file we need to modify
    """
    _image = pexif.JpegFile.fromFile(filepath)

    """
    2. Set the new value so that we have consistency across the board
    """
    _image.exif.primary.Orientation = [_new_orientation]

    """
    3. Write out the Exif data
    """
    _image.writeFile(filepath)
    logger.debug('[MEDIA utilities:orientation] Orientation verification complete, _image write complete `%s`' % (_image))


"""
Create an image according to spec
"""
def create(image, name, suffix, extension, directory, size={}):

    logger.debug('[MEDIA utilities:create] Image creation process started')

    filename = name + suffix + extension
    filepath = os.path.join(directory, 'images', filename)

    with image.clone() as temporary_image:

        if size.has_key('width') and size.has_key('height'):
            thumbnail(temporary_image, size.get('width'), size.get('height'))

        temporary_image.save(filename=filepath)

        if image.format is 'jpeg':
            orientation(filepath)

    logger.debug('[MEDIA utilities:create] Image creation process completed with filename:`%s`' % (filename))
    return filename


"""
Upload a File Object Directly to AmazonS3 and then return a URL to that image.
"""
def upload_image(source_file, acl='public-read'):

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
        logger.debug('[MEDIA utilities:upload_image] Completed creating transformable image object `%s`' % (image))
    except:
        logger.debug('[MEDIA utilities:upload_image] Exception raised while creating transformable image object')
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

        logger.debug('[MEDIA utilities:upload_image] Completed rotating original orientation')
    except:
        logger.debug('[MEDIA utilities:upload_image] Exception raised while trying to rotate original orientation')
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

        logger.debug('[MEDIA utilities:upload_image] Image upload process complete')
        return {
            'original': os.path.join(basepath, original_filename),
            'square': os.path.join(basepath, square_filename),
            'square_retina': os.path.join(basepath, square_retina_filename),
            'thumbnail': os.path.join(basepath, thumbnail_filename),
            'thumbnail_retina': os.path.join(basepath, thumbnail_retina_filename),
            'icon': os.path.join(basepath, icon_filename),
            'icon_retina': os.path.join(basepath, icon_retina_filename)
        }
    except:
        logger.debug('[MEDIA utilities:upload_image] Exception raised while trying to create multiple formats')
        raise


"""
Upload a File Object Directly to our server and then return a URL to that file
"""
def upload_file(source_file, acl='public-read'):

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
        logger.debug('[MEDIA utilities:upload_file] Saving file source information to server')
        source_file.save(filepath)
    except:
        logger.debug('[MEDIA utilities:upload_file] Exception raised while saving file source information to server')
        raise

    logger.debug('[MEDIA utilities:upload_file] File upload process completed with original:%s' % (fileurl))
    return {
        'original': fileurl
    }
