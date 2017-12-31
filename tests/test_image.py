import datetime

from tests.helper.client import *
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
    image_id = upload_response.json['id']

    response = client.simulate_get('/image', headers=client_headers())

    assert response.json == {
        'images': [image_id]
    }
    assert response.status == falcon.HTTP_OK


def test_image_get(client):
    upload_response = helper_image_upload(client)
    image_id = upload_response.json['id']

    response = client.simulate_get('/image/' + image_id, headers=client_headers())

    assert response.status == falcon.HTTP_OK
    assert 'Last-Modified' in response.headers
    assert response.content == b'abcdef'


def test_image_get_if_modified_since(client):
    upload_response = helper_image_upload(client)
    image_id = upload_response.json['id']

    headers = client_headers()
    last_modified = datetime.datetime(year=2030, month=1, day=1).strftime('%a, %d %b %Y %H:%M:%S GMT')
    headers['If-Modified-Since'] = last_modified

    response = client.simulate_get('/image/' + image_id, headers=headers)

    assert response.status == falcon.HTTP_NOT_MODIFIED


def test_image_get_if_modified_since_not(client):
    upload_response = helper_image_upload(client)
    image_id = upload_response.json['id']

    headers = client_headers()
    last_modified = datetime.datetime(year=2000, month=1, day=1).strftime('%a, %d %b %Y %H:%M:%S GMT')
    headers['If-Modified-Since'] = last_modified

    response = client.simulate_get('/image/' + image_id, headers=headers)

    assert response.status != falcon.HTTP_NOT_MODIFIED


def test_image_head(client):
    upload_response = helper_image_upload(client)
    image_id = upload_response.json['id']

    response = client.simulate_head('/image/' + image_id, headers=client_headers())

    assert response.status == falcon.HTTP_OK


def test_image_head_404(client):
    response = client.simulate_head('/image/nonExisting', headers=client_headers())

    assert response.status == falcon.HTTP_NOT_FOUND
