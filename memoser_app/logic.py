import hashlib

from django.conf import settings


def verify_openapi_auth(data):
    params = {k: v for k, v in map(lambda e: e.split('='), data.split('&'))}
    hashed = hashlib.md5()
    hashed.update('expire={expire}mid={mid}secret={secret}sid={sid}{secure_key}'.format(
        expire=params.get('expire'),
        mid=params.get('mid'),
        secret=params.get('secret'),
        sid=params.get('sid'),
        secure_key=settings.VK_SECURE_KEY,
    ).encode('utf-8'))
    return params.get('sig') and hashed.hexdigest() == params['sig']
