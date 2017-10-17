FROM python:3

WORKDIR /usr/src/app

COPY setup.py setup.py
RUN python3 setup.py install

COPY server server

ENV DB_PATH "data.json"
ENV GOOGLE_APPLICATION_CREDENTIALS "gkey.json"

ENV STORAGE_PATH "/usr/src/app/image_store"
VOLUME ["/usr/src/app/image_store"]

EXPOSE 8000

CMD [ "gunicorn", "--reload", "--bind=0.0.0.0:8000", "server.app:get_app()" ]