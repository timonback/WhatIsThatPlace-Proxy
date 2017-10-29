#!/usr/bin/env bash

HOST=0.0.0.0
PORT=8888

#sudo apt-get install python3-pip python3-dev
echo "Install requirements..."
pip3 install virtualenv
python3 -m virtualenv -p python3 env
source env/bin/activate

python3 setup.py install

export GOOGLE_APPLICATION_CREDENTIALS=gkey.json

function server_unix() {
    # On Unix
    gunicorn --bind="$HOST:$PORT" --reload 'server.app:get_app()'
}

function server_windows() {
    # On Windows
    waitress-serve --host="$HOST" -port="$PORT" "server.app:get_app()"
}

echo "Start serving the application..."
if [ "$(uname)" == "Darwin" ]; then
    server_unix
elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
    server_unix
elif [ "$(expr substr $(uname -s) 1 10)" == "MINGW32_NT" ]; then
    server_windows
elif [ "$(expr substr $(uname -s) 1 10)" == "MINGW64_NT" ]; then
    server_windows
fi
