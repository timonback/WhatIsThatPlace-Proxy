from server.middleware.authentication import AuthMiddleware
from tests.app import *


def test_auth_database(client):
    response = client.simulate_get('/database')
    assert response.status == falcon.HTTP_UNAUTHORIZED


def test_auth_database_param(client):
    response = client.simulate_get('/database',
                                   query_string='Authorization=' + AuthMiddleware.TOKEN)
    assert response.status == falcon.HTTP_OK


def test_auth_image(client):
    response = client.simulate_get('/image')
    assert response.status == falcon.HTTP_UNAUTHORIZED
