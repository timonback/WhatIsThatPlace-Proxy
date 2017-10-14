#!/bin/bash

python3 setup.py install
gunicorn --reload 'server.app:get_app()'