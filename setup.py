#!/usr/bin/env python3.6

from setuptools import setup

setup(
    name='whatisthatplace-proxy',
    version='0.0.1',
    install_requires=[
        'falcon>=1.1.0',
        'falcon-multipart',

        'grpcio<1.6',
        'google-cloud-core==0.27.0',
        'google-cloud-vision==0.27.0',

        'gunicorn', #Linux
        # 'waitress', #Windows
        'httpie', #Nice http client

        'pytest',
    ],
    url='https://github.com/timonback/whatisthatplace-proxy',
    license='MIT',
    author='',
    author_email='',
    description=''
)
