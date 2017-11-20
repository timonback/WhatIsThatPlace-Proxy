from tests.app import *
from tests.helper.multipart import *


def helper_image_upload(client, content=b'abcdef'):
    data, headers = create_multipart(content, fieldname='image',
                                     filename='image.jpg',
                                     content_type='image/jpg')
    headers.update(client_headers())

    return client.simulate_post('/image', body=data, headers=headers)
