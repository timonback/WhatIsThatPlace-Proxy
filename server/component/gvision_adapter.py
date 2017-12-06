import logging

logger = logging.getLogger(__name__)


class GVisionClient:
    """
    Adapter that can be mocked for testing
    """

    def __init__(self, client=None):
        if client is None:
            from google.cloud.vision import ImageAnnotatorClient
            client = ImageAnnotatorClient()
        self._client = client

    def landmark_detection(self, image):
        gresponse = self._client.landmark_detection(image=image)
        logger.debug('Raw Response {}'.format(gresponse))

        res_landmarks = []
        for landmark in gresponse.landmark_annotations:

            res_vertices = []
            for vortex in landmark.bounding_poly.vertices:
                res_vortex = {
                    'x': vortex.x,
                    'y': vortex.y,
                }
                res_vertices.append(res_vortex)
            res_bounding_poly = {
                'vertices': res_vertices
            }

            res_locations = []
            for location in landmark.locations:
                lat_lng = location.lat_lng
                print('Latitude'.format(lat_lng.latitude))
                print('Longitude'.format(lat_lng.longitude))

                res_location = {
                    'latitude': lat_lng.latitude,
                    'longitude': lat_lng.longitude,
                }
                res_locations.append(res_location)
            res_landmark = {
                'mid': landmark.mid,
                'description': landmark.description,
                'score': landmark.score,
                'locations': res_locations,
                'bounding_poly': res_bounding_poly,
            }
            res_landmarks.append(res_landmark)

        response = {}
        response['landmarks'] = res_landmarks
        return response
