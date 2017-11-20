from tests.helper.client import *
from tests.helper.headers import *


def test_database_empty(client):
    response = client.simulate_get('/database', headers=client_headers())

    assert response.json == {}
    assert response.status == falcon.HTTP_OK
