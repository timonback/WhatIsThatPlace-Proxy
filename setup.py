from setuptools import setup

setup(
    name='whatisthatplace-proxy',
    version='0.0.1',
    install_requires=[
        'falcon>=1.1.0',
        'msgpack-python>=0.4.8',
        'google-cloud-vision>=0.27.0',
        'msgpack-python',

        'gunicorn', #Linux
        'waitress', #Windows
        'httpie', #Nice http client
    ],
    url='https://github.com/timonback/whatisthatplace-proxy',
    license='MIT',
    author='',
    author_email='',
    description=''
)
