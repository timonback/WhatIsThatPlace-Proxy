import json


class GVisionApiMock:
    def landmark_detection(self, image):
        with open('tests/data/vision.json') as visionDump:
            content = json.load(visionDump)
            return {
                'landmark_annotations': content['landmarkAnnotations']
            }
