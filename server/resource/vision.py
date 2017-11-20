import falcon
import json

from server.resource.image import CollectionItem


class Vision:
    PATH = CollectionItem.PATH + '/landmark'

    def __init__(self, vision_api):
        self._vision_api = vision_api

    def on_get(self, req, resp, name):
        try:
            response = self._vision_api.analyse(name)

            resp.body = json.dumps(response, ensure_ascii=False)
            resp.content_type = falcon.MEDIA_JSON
            resp.status = falcon.HTTP_200
        except IOError:
            resp.status = falcon.HTTP_NOT_FOUND
