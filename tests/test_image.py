from tests.app import *


def test_image_upload(client):
    data, headers = create_multipart(b'abcdef', fieldname='image',
                                     filename='image.jpg',
                                     content_type='image/jpg')
    headers.update(client_headers())

    response = client.simulate_post('/image', body=data, headers=headers)

    assert response.status == falcon.HTTP_CREATED
