import logging
import os

import falcon

from server.component.image_store import ImageStore
from server.component.json_db import JsonDB
from server.component.vision_api import VisionApi
from server.resource.image import Collection, Item
from server.resource.vision import Vision
from server.util.logger import setup_logger

logger = logging.getLogger(__name__)


def create_app(image_store, vision_api):
    setup_logger('output.log')

    api = falcon.API()

    collection = Collection(image_store)
    api.add_route('/image/{name}', Item(image_store))

    api.add_route(collection.PATH, collection)
    api.add_route('/vision/{name}', Vision(vision_api))

    return api


def get_app():
    db_path = os.environ.get('DB_PATH', 'data.json')
    db = JsonDB(db_path)

    storage_path = os.environ.get('STORAGE_PATH', '.')
    image_store = ImageStore(storage_path, db)
    vision_api = VisionApi(db, image_store)
    return create_app(image_store, vision_api)
