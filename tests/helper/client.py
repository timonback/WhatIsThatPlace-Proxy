import pytest
from falcon import testing

from server.app import *
from server.component.vision_api import VisionApi
from tests.mock.vision_api import GVisionApiMock


@pytest.fixture
def client():
    db_file = 'data_test.json'
    if os.path.isfile(db_file):
        os.remove(db_file)
    if not os.path.isdir('tmp'):
        os.mkdir('tmp')

    db = create_app_db(db_file)
    image_store = create_app_image_storage('tmp/', db)
    vision_api_adapter = GVisionApiMock()
    vision_api = VisionApi(db, image_store, vision_api_adapter)
    api = create_app(db, image_store, vision_api)

    return testing.TestClient(api)
