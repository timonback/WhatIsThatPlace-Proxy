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
                self.db = json.load(json_data)
        except FileNotFoundError:
            logger.warning(f"Could not open database file {self.filename}")


    def get(self, key):
        if key in self.db.keys():
            return self.db[key]
        return {}

    def save(self):
        with open(self.filename, 'w') as outfile:
            json.dump(self.db, outfile)

    def set(self, key, value, overwrite=True):
        if key in self.db.keys() and overwrite is False:
            return None
        self.db[key] = value

        self.save()

        return value
