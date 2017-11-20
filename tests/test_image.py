from tests.helper.image_upload import *

def test_image_upload(client):
    response = helper_image_upload(client)

    assert response.status == falcon.HTTP_CREATED
    assert response.json == {'id': 'e80b5017098950fc58aad83c8c14978e'}


def test_image_list_empty(client):
    response = client.simulate_get('/image', headers=client_headers())

    assert response.json == {'images': []}
    assert response.status == falcon.HTTP_OK


def test_image_list(client):
    upload_response = helper_image_upload(client)

    response = client.simulate_get('/image', headers=client_headers())

    assert response.json == {
        'images': [upload_response.json['id']]
    }
    assert response.status == falcon.HTTP_OK


def test_image_get(client):
    upload_response = helper_image_upload(client)
    image_id = upload_response.json['id']

    response = client.simulate_get('/image/' + image_id, headers=client_headers())

    assert response.status == falcon.HTTP_OK
    assert response.content == b'abcdef'
