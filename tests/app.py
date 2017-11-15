import pytest
from falcon import testing

from server.app import *
from tests.mock.vision_api import VisionApiMock


@pytest.fixture
def client():
    db = create_app_db()
    image_store = create_app_image_storage(db)
    vision_api = VisionApiMock(db, image_store)
    api = create_app(db, image_store, vision_api)

    return testing.TestClient(api)


def client_headers():
    return {
        'Authorization': '988c4dcf-d7d2-45f1-b4ec-9123a0ab61d1'
    }
