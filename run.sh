#!/usr/bin/env bash

HOST=0.0.0.0
PORT=8000

python3.6 setup.py install

export GOOGLE_APPLICATION_CREDENTIALS=gkey.json

function server_unix() {
    # On Unix
    gunicorn --bind="$HOST:$PORT" --reload 'server.app:get_app()'
}

function server_windows() {
    # On Windows
    waitress-serve --host="$HOST" -port="$PORT" "server.app:get_app()"
}

if [ "$(uname)" == "Darwin" ]; then
    server_unix
elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
    server_unix
elif [ "$(expr substr $(uname -s) 1 10)" == "MINGW32_NT" ]; then
    server_windows
elif [ "$(expr substr $(uname -s) 1 10)" == "MINGW64_NT" ]; then
    server_windows
fi
