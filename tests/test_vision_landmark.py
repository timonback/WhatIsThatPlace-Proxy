from tests.helper.client import *
from tests.helper.image_upload import *


def test_image_get(client):
    upload_response = helper_image_upload(client)
    image_id = upload_response.json['id']

    response = client.simulate_get('/image/' + image_id + '/landmark',
                                   headers=client_headers())

    assert response.status == falcon.HTTP_OK
    assert response.json != ''
