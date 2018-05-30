import os
import json

class Config(object):

    with open('/root/keys.json', 'r') as f:
        client_id = json.load(f)['DISCORD_OAUTH_CLIENT_ID']
        client_secret = json.load(f)['DISCORD_OAUTH_CLIENT_SECRET']
        secret = json.load(f)['SECRET']

    SECRET_KEY = os.environ.get('SECRET_KEY') or secret

    DISCORD_OAUTH_CLIENT_ID = os.environ.get('DISCORD_OAUTH_CLIENT_ID') or client_id
    DISCORD_OAUTH_CLIENT_SECRET = os.environ.get('DISCORD_OAUTH_CLIENT_SECRET') or client_secret
