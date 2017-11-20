import json
import logging
import threading

from google.cloud.vision import types

logger = logging.getLogger(__name__)


class VisionApi:
    _DB_KEY = 'VISION_API'
    _DB_QUOTA_KEY = 'QUOTA'
    _DB_QUOTA_DEFAULT = 1000

    quota_lock = threading.Lock()

    def __init__(self, db, image_store, client):
        self._db = db
        self._image_store = image_store
        self._client = client

    def analyse(self, identifier):
        db_response = self._load_from_db(identifier)
        if db_response is None:
            quota = self._load_from_db(self._DB_QUOTA_KEY)
            if quota == 0:
                logger.warning('Quota is exceeded!')
                return {'error': 'Quota is exceeded'}

            image_file, length, filename = self._image_store.open(identifier)
            content = image_file.read()
            db_response = self._execute(identifier, content)
        return db_response

    def _execute(self, identifier, file_content):
        image = types.Image(content=file_content)

        self._reduce_quota()

        # Performs label detection on the image file
        response = self._client.landmark_detection(image=image)
        logger.debug('Response {}'.format(response))

        self._save_to_db(identifier, response)

        return response

    def _reduce_quota(self):
        with self.quota_lock:
            quota = self._load_from_db(self._DB_QUOTA_KEY)
            if quota is None:
                quota = self._DB_QUOTA_DEFAULT
            quota = quota - 1
            self._save_to_db(self._DB_QUOTA_KEY, quota)

    def _load_from_db(self, identifier):
        if self._db:
            db_obj = self._db.get(self._DB_KEY)
            if identifier in db_obj.keys():
                return json.loads(db_obj[identifier])
        return None

    def _save_to_db(self, identifier, response):
        if self._db:
            db_obj = self._db.get(self._DB_KEY)
            db_obj[identifier] = json.dumps(response, default=lambda o: o.__dict__)
            self._db.set(self._DB_KEY, db_obj)
