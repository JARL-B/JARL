import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'very secret key'

    DISCORD_OAUTH_CLIENT_ID = os.environ.get('DISCORD_OAUTH_CLIENT_ID') or '440052776702312450'
    DISCORD_OAUTH_CLIENT_SECRET = os.environ.get('DISCORD_OAUTH_CLIENT_SECRET') or 'FjMSodOATz4FoXByylp6QS0lWQLeYKWa'
