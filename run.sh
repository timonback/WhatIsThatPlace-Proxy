#!/bin/bash

python3 setup.py install

export GOOGLE_APPLICATION_CREDENTIALS=gkey.json
gunicorn --reload 'server.app:get_app()'