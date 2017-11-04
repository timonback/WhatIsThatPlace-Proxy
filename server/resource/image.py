import falcon
import json
import mimetypes

class Collection(object):
    PATH = '/image'
    PARAM_IMAGE = 'image'

    def __init__(self, image_store):
        self._image_store = image_store

    def on_get(self, req, resp):
        doc = {
            'images': self._image_store.get_all()
        }

        resp.body = json.dumps(doc, ensure_ascii=False)
        resp.content_type = falcon.MEDIA_JSON
        resp.status = falcon.HTTP_200

    def on_post(self, req, resp):
        image = req.get_param(self.PARAM_IMAGE)

        name = self._image_store.save(image.file)
        resp.status = falcon.HTTP_201
        resp.location = self.PATH + name


class CollectionItem(object):
    PATH = Collection.PATH + '/{name}'

    def __init__(self, image_store):
        self._image_store = image_store

    def on_get(self, req, resp, name):
        resp.content_type = mimetypes.guess_type(name)[0]
        try:
            resp.stream, resp.stream_len = self._image_store.open(name)
        except IOError:
            # Normally you would also log the error.
            raise falcon.HTTPNotFound()
