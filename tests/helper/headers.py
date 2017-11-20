from server.middleware.authentication import AuthMiddleware


def client_headers():
    return {
        'Authorization': AuthMiddleware.TOKEN
    }
