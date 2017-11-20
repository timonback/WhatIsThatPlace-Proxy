from tests.helper.client import *
from tests.helper.headers import *


def test_auth_database(client):
    response = client.simulate_get('/database')
    assert response.status == falcon.HTTP_UNAUTHORIZED


def test_auth_database_header(client):
    response = client.simulate_get('/database', headers=client_headers())
    assert response.status == falcon.HTTP_OK


def test_auth_database_param(client):
    auth_query = 'Authorization=' + client_headers()['Authorization']
    response = client.simulate_get('/database', query_string=auth_query)
    assert response.status == falcon.HTTP_OK


def test_auth_image(client):
    response = client.simulate_get('/image')
    assert response.status == falcon.HTTP_UNAUTHORIZED
