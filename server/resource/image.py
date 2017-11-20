import falcon
import json


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
        if image is None:
            raise falcon.HTTPBadRequest('No file passed to the {} parameter'.format(
                self.PARAM_IMAGE))

        file_id = self._image_store.save(image.file, image.filename)
        resp.status = falcon.HTTP_CREATED
        resp.media = {'id': file_id}
        resp.location = self.PATH + '/' + file_id


class CollectionItem(object):
    PATH = Collection.PATH + '/{name}'

    def __init__(self, image_store):
        self._image_store = image_store

    def on_get(self, req, resp, name):
        resp.content_type = 'image/*'
        try:
            resp.stream, resp.stream_len, filename = self._image_store.open(name)
            resp.append_header('Content-Disposition',
                               'inline; filename="' + filename + '"')
            resp.status = falcon.HTTP_OK
        except IOError:
            # Normally you would also log the error.
            raise falcon.HTTPNotFound()

    def on_head(self, req, resp, name):
        if self._image_store.contains(name):
            resp.status = falcon.HTTP_200
        else:
            resp.status = falcon.HTTP_NOT_FOUND
