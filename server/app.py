import os
import logging

import falcon

from .image_store import ImageStore
from .images import Collection, Item
from .json_db import JsonDB
from .util.logger import setup_logger


logger = logging.getLogger(__name__)


def create_app(image_store):
    setup_logger('output.log')

    api = falcon.API()
    api.add_route('/images', Collection(image_store))
    api.add_route('/images/{name}', Item(image_store))
    return api


def get_app():
    db = JsonDB('data.json')

    storage_path = os.environ.get('LOOK_STORAGE_PATH', '.')
    image_store = ImageStore(storage_path, db)
    return create_app(image_store)
