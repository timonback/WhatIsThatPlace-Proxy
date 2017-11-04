import falcon
import json


class Vision:
    PATH = '/vision/{name}'

    def __init__(self, vision_api):
        self._vision_api = vision_api

    def on_get(self, req, resp, name):
        response = self._vision_api.analyse(name)

        resp.body = json.dumps(response, ensure_ascii=False)
        resp.content_type = falcon.MEDIA_JSON
        resp.status = falcon.HTTP_200
