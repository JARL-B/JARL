import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'very secret key'

    DISCORD_OAUTH_CLIENT_ID = os.environ.get('DISCORD_OAUTH_CLIENT_ID') or ''
    DISCORD_OAUTH_SECRET_KEY = os.environ.get('DISCORD_OAUTH_SECRET_KEY') or ''
