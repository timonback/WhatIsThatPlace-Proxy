import json
import logging

logger = logging.getLogger(__name__)


class JsonDB:
    def __init__(self, db_filename):
        self.filename = db_filename
        self.db = {}

        self.open()

    def open(self):
        try:
            with open(self.filename) as json_data:
                try:
                    self.db = json.load(json_data)
                except ValueError:
                    logger.warning(f"Could not parse the data in {self.filename}")
                    self.db = {}
        except FileNotFoundError:
            logger.warning(f"Could not open database file {self.filename}")

    def get(self, key):
        if key in self.db.keys():
            return self.db[key]
        return {}

    def keys(self):
        return self.db.keys()

    def save(self):
        with open(self.filename, 'w') as outfile:
            json.dump(self.db, outfile,
                      sort_keys=True, indent=2, separators=(',', ': '))

    def set(self, key, value, overwrite=True):
        if not self._is_jsonable(key):
            logger.error(f"The key is not saveable {key}")
            return
        if not self._is_jsonable(value):
            logger.error(f"The value is not saveable {value}")
            return

        if key in self.db.keys() and overwrite is False:
            return None
        self.db[key] = value

        self.save()

        return value

    @staticmethod
    def _is_jsonable(x):
        try:
            json.dumps(x)
            return True
        except:
            return False
