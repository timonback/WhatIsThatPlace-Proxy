import hashlib
import io
import logging
import os
import re
import uuid

logger = logging.getLogger(__name__)


class ImageStore(object):
    _CHUNK_SIZE_BYTES = 4096
    _IMAGE_NAME_PATTERN = re.compile(
        '[0-9a-f]{32}$'
    )
    _DB_KEY = 'IMAGE_STORE'

    def __init__(self, storage_path, db=None, uuidgen=uuid.uuid4, fopen=io.open):
        self._storage_path = storage_path
        self._db = db
        self._uuidgen = uuidgen
        self._fopen = fopen

    def get_all(self):
        items = []
        if self._db:
            db_obj = self._db.get(self._DB_KEY)
            for item in db_obj.keys():
                items.append(item)

        return items

    def open(self, name):
        logger.info('Requested image {name}'.format(name=name))

        # Always validate untrusted input!
        if not self._IMAGE_NAME_PATTERN.match(name):
            raise IOError('Requested image {name} - invalid'.format(name=name))

        if self._db:
            db_obj = self._db.get(self._DB_KEY)
            if name in db_obj:
                image_file = db_obj[name]
                logger.debug('Requested image {name} - found'.format(name=name))
                return self._get_stream(image_file)
        logger.debug('Requested image {name} - fallback'.format(name=name))
        return self._get_stream(name)

    def _get_stream(self, image_name):
        image_path = os.path.join(self._storage_path, image_name)
        stream = self._fopen(image_path, 'rb')
        stream_len = os.path.getsize(image_path)

        return stream, stream_len, image_name

    def save(self, file, filename):
        logger.info('Storing incoming image')

        ext = None
        if filename is not None and len(filename) > 1:
            ext = os.path.splitext(filename)[1]
        image_upload_path = '{folder}/{uuid}{ext}'.format(folder=self._storage_path,
                                                          uuid=self._uuidgen(),
                                                          ext=ext)
        file_hash = hashlib.md5()
        with self._fopen(image_upload_path, 'wb') as image_file:
            while True:
                chunk = file.read(self._CHUNK_SIZE_BYTES)
                if not chunk:
                    break

                image_file.write(chunk)
                file_hash.update(chunk)

        image_id = file_hash.hexdigest()
        image_real_path = '{folder}/{name}{ext}'.format(folder=self._storage_path,
                                                        name=image_id,
                                                        ext=ext)
        image_real_name = '{name}{ext}'.format(name=image_id, ext=ext)

        if self._db:
            key = image_id
            db_obj = self._db.get(self._DB_KEY)
            logger.debug('{}'.format(db_obj))

            if key in db_obj:
                logger.info('This file was already uploaded before')
            else:
                if not os.path.isfile(image_real_path):
                    os.rename(image_upload_path, image_real_path)
                else:
                    os.remove(image_upload_path)
                db_obj[key] = image_real_name
                self._db.set(self._DB_KEY, db_obj)

        logger.info('Image has identifier: {name}'.format(name=image_id))
        return image_id
