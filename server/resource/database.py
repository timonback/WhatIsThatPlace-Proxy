import json

import falcon


class Database(object):
    PATH = '/database/'

    def __init__(self, json_db):
        self.json_db = json_db

    def on_get(self, req, resp):
        resp.body = json.dumps(self.json_db.db, ensure_ascii=False)
        resp.content_type = falcon.MEDIA_JSON
        resp.status = falcon.HTTP_200
