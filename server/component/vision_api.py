import json
import logging

from google.cloud.vision import ImageAnnotatorClient, types

logger = logging.getLogger(__name__)


class VisionApi:
    _DB_KEY = "VISION_API"

    def __init__(self, db, image_store):
        self._db = db
        self._image_store = image_store

        self._client = ImageAnnotatorClient()

    def analyse(self, identifier):
        db_response = self._load_from_db(identifier)
        if db_response is None:
            image_file, length = self._image_store.open(identifier)
            content = image_file.read()
            db_response = self._execute(identifier, content)
        return db_response

    def _execute(self, identifier, file_content):
        image = types.Image(content=file_content)

        # Performs label detection on the image file
        gresponse = self._client.landmark_detection(image=image)

        response = {}

        print('Landmarks:')
        res_landmarks = []
        for landmark in gresponse.landmark_annotations:
            print(landmark.description)

            res_vertices = []
            for vortex in landmark.bounding_poly.vertices:
                res_vortex = {
                    "x": vortex.x,
                    "y": vortex.y,
                }
                res_vertices.append(res_vortex)
            res_bounding_poly = {
                "vertices": res_vertices
            }

            res_locations = []
            for location in landmark.locations:
                lat_lng = location.lat_lng
                print('Latitude'.format(lat_lng.latitude))
                print('Longitude'.format(lat_lng.longitude))

                res_location = {
                    "latitude": lat_lng.latitude,
                    "longitude": lat_lng.longitude,
                }
                res_locations.append(res_location)
            res_landmark = {
                "mid": landmark.mid,
                "description": landmark.description,
                "score": landmark.score,
                "locations": res_locations,
                "bounding_poly": res_bounding_poly,
            }
            res_landmarks.append(res_landmark)

        response["landmarks"] = res_landmarks

        self._save_to_db(identifier, response)

        return response

    def _load_from_db(self, identifier):
        if self._db:
            db_obj = self._db.get(self._DB_KEY)
            if identifier in db_obj.keys():
                return json.loads(db_obj[identifier])
        return None

    def _save_to_db(self, identifier, response):
        if self._db:
            db_obj = self._db.get(self._DB_KEY)
            db_obj[identifier] = json.dump(response)
            self._db.set(self._DB_KEY, db_obj)
