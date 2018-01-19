# WhatisthatPlace-Proxy

This is a small proxy/caching application to stand between an application and the Google Vision API. This shall ensure that the same image is only analyzed once (save money) and to allow an easy exchange of the associated google project instead of having to redeploy another application (mobile application) that might take some days.

## Prerequisite
Ensure to create and download your Google Creditials (JSON file) place it in the root folder as gkey.json.

You can get them from [https://console.cloud.google.com/apis/credentials](https://console.cloud.google.com/apis/credentials). They are called Service account keys. Also enable the Vision API if you havent done so at [https://console.cloud.google.com/apis/api/vision.googleapis.com/overview](https://console.cloud.google.com/apis/api/vision.googleapis.com/overview).

## Run
Create a virtual environment
```
virtualenv -p python3.6 envlinux
source envlinux/bin/activate
```

Just run ```run.sh```

The python dependencies will be installed automatically.

## Security
Make sure to protect your server. This proxy server requires an authentication token, when you move out of the testing phase, change it! [https://github.com/timonback/WhatisthatPlace-Proxy/blob/master/server/middleware/authentication.py](https://github.com/timonback/WhatisthatPlace-Proxy/blob/master/server/middleware/authentication.py)
