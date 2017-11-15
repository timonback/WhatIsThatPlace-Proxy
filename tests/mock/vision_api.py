class VisionApiMock:
    def __init__(self, db, image_store):
        self._db = db
        self._image_store = image_store

    def analyse(self, identifier):
        return identifier
