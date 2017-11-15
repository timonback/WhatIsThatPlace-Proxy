from tests.app import *


def test_empty_database(client):
    doc = {}

    response = client.simulate_get('/database', headers=client_headers())

    assert response.json == doc
    assert response.status == falcon.HTTP_OK
