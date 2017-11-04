import falcon
import json
import mimetypes


class ImageTypeValidator:
    ALLOWED_IMAGE_TYPES = (
        'image/gif',
        'image/jpeg',
        'image/jpg',
        'image/png',
    )

    @classmethod
    def validate_image_type(cls, req, resp, resource, params):
        if req.content_type not in cls.ALLOWED_IMAGE_TYPES:
            msg = 'Image type not allowed. Must be PNG, JPEG, or GIF'
            raise falcon.HTTPBadRequest('Bad request', msg)


class Collection(object):
    PATH = '/image'

    def __init__(self, image_store):
        self._image_store = image_store

    def on_get(self, req, resp):
        doc = {
            'images': self._image_store.get_all()
        }

        resp.body = json.dumps(doc, ensure_ascii=False)
        resp.content_type = falcon.MEDIA_JSON
        resp.status = falcon.HTTP_200

    @falcon.before(ImageTypeValidator.validate_image_type)
    def on_post(self, req, resp):
        name = self._image_store.save(req.stream, req.content_type)
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
