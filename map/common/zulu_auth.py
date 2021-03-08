"""
Module preparing credentials for zulu server
"""

from base64 import b64encode

from WebZulu.settings import ZULU_USER, ZULU_PWD


def get_credentials():
    """
    prepare credentials for base authorization in zulu server
    :return: str
    """
    return b64encode((ZULU_USER + ':' + ZULU_PWD).encode('ascii')).decode('ascii')
