import falcon
import logging
import os
from falcon_multipart.middleware import MultipartMiddleware

from server.component.image_store import ImageStore
from server.component.json_db import JsonDB
from server.middleware.authentication import AuthMiddleware
from server.middleware.require_json import RequireJSON
from server.resource.database import Database
from server.resource.image import Collection, CollectionItem
from server.resource.vision import Vision
from server.util.logger import setup_logger

logger = logging.getLogger(__name__)


def create_app(db, image_store, vision_api):
    setup_logger('output.log')

    api = falcon.API(
        middleware=[
            AuthMiddleware(),
            MultipartMiddleware(),
            RequireJSON()
        ]
    )

    database = Database(db)
    api.add_route(database.PATH, database)

    collection = Collection(image_store)
    api.add_route(collection.PATH, collection)
    api.add_route(CollectionItem.PATH, CollectionItem(image_store))

    api.add_route(Vision.PATH, Vision(vision_api))
    return api


def create_app_db():
    db_path = os.environ.get('DB_PATH', 'data.json')
    db = JsonDB(db_path)
    return db


def create_app_image_storage(db):
    storage_path = os.environ.get('STORAGE_PATH', '.')
    image_store = ImageStore(storage_path, db)
    return image_store


def get_app():
    # hack to allow tests without google vision api
    from server.component.vision_api import VisionApi

    db = create_app_db()
    image_store = create_app_image_storage(db)
    vision_api = VisionApi(db, image_store)
    return create_app(db, image_store, vision_api)
