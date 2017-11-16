import io
import pytest
import random
import string
from falcon import testing

from server.app import *
from server.middleware.authentication import AuthMiddleware
from tests.mock.vision_api import VisionApiMock


@pytest.fixture
def client():
    db_file = 'data_test.json'
    if os.path.isfile(db_file):
        os.remove(db_file)
    if not os.path.isdir('tmp'):
        os.mkdir('tmp')

    db = create_app_db(db_file)
    image_store = create_app_image_storage('tmp/', db)
    vision_api = VisionApiMock(db, image_store)
    api = create_app(db, image_store, vision_api)

    return testing.TestClient(api)


def client_headers():
    return {
        'Authorization': AuthMiddleware.TOKEN
    }


def create_multipart(data, fieldname, filename, content_type):
    """
    Basic emulation of a browser's multipart file upload
    """
    boundry = '----WebKitFormBoundary' + ''.join(random.choice(string.ascii_lowercase)
                                                 for _ in range(16))
    buff = io.BytesIO()
    buff.write(b'--')
    buff.write(boundry.encode())
    buff.write(b'\r\n')
    buff.write(('Content-Disposition: form-data; name="%s"; filename="%s"' % \
                (fieldname, filename)).encode())
    buff.write(b'\r\n')
    buff.write(('Content-Type: %s' % content_type).encode())
    buff.write(b'\r\n')
    buff.write(b'\r\n')
    buff.write(data)
    headers = {'Content-Type': 'multipart/form-data; boundary=%s' % boundry}
    headers['Content-Length'] = str(buff.tell())
    return buff.getvalue(), headers
