import hashlib
import io
import logging
import mimetypes
import os
import re
import uuid

logger = logging.getLogger(__name__)


class ImageStore(object):
    _CHUNK_SIZE_BYTES = 4096
    _IMAGE_NAME_PATTERN = re.compile(
        '[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\.[a-z]{2,4}$'
    )
    _DB_KEY = "IMAGE_STORE"

    def __init__(self, storage_path, db=None, uuidgen=uuid.uuid4, fopen=io.open):
        self._storage_path = storage_path
        self._db = db
        self._uuidgen = uuidgen
        self._fopen = fopen

    def get_all(self):
        items = []
        if self._db:
            db_obj = self._db.get(self._DB_KEY)
            for item in db_obj.values():
                items.append(item)

        return items

    def open(self, name):
        logger.info(f"Returning file {name}")

        # Always validate untrusted input!
        if not self._IMAGE_NAME_PATTERN.match(name):
            raise IOError('File not found')

        image_path = os.path.join(self._storage_path, name)
        stream = self._fopen(image_path, 'rb')
        stream_len = os.path.getsize(image_path)

        return stream, stream_len

    def save(self, image_stream, image_content_type):
        logger.info(f"Storing incoming image")

        ext = mimetypes.guess_extension(image_content_type)
        name = '{uuid}{ext}'.format(uuid=self._uuidgen(), ext=ext)
        image_path = os.path.join(self._storage_path, name)

        file_hash = hashlib.md5()

        with self._fopen(image_path, 'wb') as image_file:
            while True:
                chunk = image_stream.read(self._CHUNK_SIZE_BYTES)
                if not chunk:
                    break

                image_file.write(chunk)
                file_hash.update(chunk)

        if self._db:
            key = file_hash.hexdigest()
            db_obj = self._db.get(self._DB_KEY)
            logger.debug(f"{db_obj}")

            if key in db_obj:
                logger.info(f"This file was already uploaded before")
                os.remove(image_path)
                name = db_obj[key]
            else:
                db_obj[key] = name
                self._db.set(self._DB_KEY, db_obj)

        logger.info(f"Image uses as identifier: {name}")
        return name