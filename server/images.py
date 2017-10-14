import mimetypes

import falcon
import msgpack


class ImageTypeValidator:
    ALLOWED_IMAGE_TYPES = (
        'image/gif',
        'image/jpeg',
        'image/png',
    )

    @classmethod
    def validate_image_type(cls, req, resp, resource, params):
        if req.content_type not in cls.ALLOWED_IMAGE_TYPES:
            msg = 'Image type not allowed. Must be PNG, JPEG, or GIF'
            raise falcon.HTTPBadRequest('Bad request', msg)


class Collection(object):
    def __init__(self, image_store):
        self._image_store = image_store

    def on_get(self, req, resp):
        doc = {
            'images': [
                {
                    'href': '/images/1eaf6ef1-7f2d-4ecc-a8d5-6e8adba7cc0e.png'
                }
            ]
        }

        resp.data = msgpack.packb(doc, use_bin_type=True)
        resp.content_type = 'application/msgpack'
        resp.status = falcon.HTTP_200

    @falcon.before(ImageTypeValidator.validate_image_type)
    def on_post(self, req, resp):
        name = self._image_store.save(req.stream, req.content_type)
        resp.status = falcon.HTTP_201
        resp.location = '/images/' + name


class Item(object):
    def __init__(self, image_store):
        self._image_store = image_store

    def on_get(self, req, resp, name):
        resp.content_type = mimetypes.guess_type(name)[0]
        try:
            resp.stream, resp.stream_len = self._image_store.open(name)
        except IOError:
            # Normally you would also log the error.
            raise falcon.HTTPNotFound()


