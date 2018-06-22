import os
import configparser

class Config(object):
    base_uri = '../'

    config = configparser.SafeConfigParser()
    config.read(base_uri + 'config.ini')
    client_id = config.get('WEB', 'DISCORD_OAUTH_CLIENT_ID')
    client_secret = config.get('WEB', 'DISCORD_OAUTH_CLIENT_SECRET')
    secret = config.get('WEB', 'SECRET')
    token = config.get('DEFAULT', 'token')

    SECRET_KEY = os.environ.get('SECRET_KEY') or secret

    DISCORD_OAUTH_CLIENT_ID = os.environ.get('DISCORD_OAUTH_CLIENT_ID') or client_id
    DISCORD_OAUTH_CLIENT_SECRET = os.environ.get('DISCORD_OAUTH_CLIENT_SECRET') or client_secret

    BOT_TOKEN = token
