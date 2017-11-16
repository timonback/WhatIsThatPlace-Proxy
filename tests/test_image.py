from tests.app import *

def test_image_upload(client):
    data, headers = create_multipart(b'abcdef', fieldname='image',
                                     filename='image.jpg',
                                     content_type='image/jpg')
    headers.update(client_headers())

    response = client.simulate_post('/image', body=data, headers=headers)

    assert response.status == falcon.HTTP_CREATED
    assert response.json == {'id': 'e80b5017098950fc58aad83c8c14978e'}
    return response


def test_image_list_empty(client):
    response = client.simulate_get('/image', headers=client_headers())

    assert response.json == {'images': []}
    assert response.status == falcon.HTTP_OK


def test_image_list(client):
    upload_response = test_image_upload(client)

    response = client.simulate_get('/image', headers=client_headers())

    assert response.json == {
        'images': [upload_response.json['id']]
    }
    assert response.status == falcon.HTTP_OK


def test_image_get(client):
    upload_response = test_image_upload(client)
    image_id = upload_response.json['id']
    print(image_id)

    response = client.simulate_get('/image/' + image_id, headers=client_headers())

    assert response.status == falcon.HTTP_OK
    assert response.content == b'abcdef'
