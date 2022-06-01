import os
import json


def is_hosted():
    return f'{os.path.expanduser("~")}/public_html/static/'


def is_dev(base_dir: str) -> bool:
    config_file = os.path.join(base_dir, '..', 'config.json')
    with open(config_file, 'r') as config:
        debug_conf = json.load(config)['DEBUG']
        return debug_conf


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


def get_secret_key(base_dir: str) -> str:
    config_file = os.path.join(base_dir, '..', 'config.json')
    with open(config_file, 'r') as config:
        secret_key = json.load(config)['SECRET_KEY']
        return secret_key


def get_email_conf(base_dir: str) -> dict:
    config_file = os.path.join(base_dir, '..', 'config.json')
    with open(config_file, 'r') as config:
        email_conf = json.load(config)['EMAIL_CONF']
        return email_conf


def get_allowed_hosts(base_dir: str) -> list:
    config_file = os.path.join(base_dir, '..', 'config.json')
    with open(config_file, 'r') as config:
        allowed_hosts = json.load(config)['ALLOWED_HOSTS']
        return allowed_hosts


def get_secure_ssl_redirect(base_dir: str) -> bool:
    config_file = os.path.join(base_dir, '..', 'config.json')
    with open(config_file, 'r') as config:
        secure_ssl_redirect = json.load(config)['SECURE_SSL_REDIRECT']
        return secure_ssl_redirect


def get_db_settings(base_dir: str) -> dict:
    config_file = os.path.join(base_dir, '..', 'config.json')
    with open(config_file, 'r') as config:
        db_settings = json.load(config)['DB_SETTINGS']
        return db_settings

