import os
import json


def is_hosted():
    return f'{os.path.expanduser("~")}/public_html/static/'


def is_dev() -> bool:
    debug = os.environ.get("DEBUG")
    if debug == 'True':
        return True
    else:
        return False


def get_secret_key() -> str:
    secret_key = str(os.environ.get("SECRET_KEY"))
    return secret_key


def get_allowed_hosts(base_dir: str) -> list:
    allowed_hosts = os.environ.get("DJANGO_ALLOWED_HOSTS").split(" ")
    return allowed_hosts


def get_secure_ssl_redirect() -> bool:
    ssl_redirect = os.environ.get("SECURE_SSL_REDIRECT")
    if ssl_redirect == 'True':
        return True
    else:
        return False    


def get_db_setting(title: str) -> str:
    return str(os.environ.get(title))


def get_static_root(base_dir: str) -> str:
    if is_hosted():
        return os.path.join(base_dir, '..', 'static')
    return os.path.join(base_dir, 'static')


def get_media_root(base_dir: str) -> str:
    if is_hosted():
        return os.path.join(base_dir, '..', 'media')
    return os.path.join(base_dir, 'media')


def get_path_for_qr(base_dir: str) -> str:
    if is_hosted():
        return os.path.join(base_dir, '..', 'media', 'for_qr')
    return os.path.join(base_dir, 'media', 'for_qr')




