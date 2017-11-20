import io
import random
import string


def create_multipart(data, fieldname, filename, content_type):
    """
    Basic emulation of a browser's multipart file upload
    """
    boundry = '----WebKitFormBoundary' + ''.join(random.choice(string.ascii_lowercase)
                                                 for _ in range(16))
    buff = io.BytesIO()
    buff.write(b'--')
    buff.write(boundry.encode())
    buff.write(b'\r\n')
    buff.write(('Content-Disposition: form-data; name="%s"; filename="%s"' % \
                (fieldname, filename)).encode())
    buff.write(b'\r\n')
    buff.write(('Content-Type: %s' % content_type).encode())
    buff.write(b'\r\n')
    buff.write(b'\r\n')
    buff.write(data)
    headers = {'Content-Type': 'multipart/form-data; boundary=%s' % boundry}
    headers['Content-Length'] = str(buff.tell())
    return buff.getvalue(), headers
