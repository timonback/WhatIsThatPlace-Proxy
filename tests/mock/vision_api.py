import json


class VisionApiMock:
    def __init__(self, db, image_store):
        self._db = db
        self._image_store = image_store

    def analyse(self, identifier):
        with open('tests/data/vision.json') as visionDump:
            return json.load(visionDump)['landmarkAnnotations']
