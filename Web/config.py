import os
import json

class Config(object):

    with open('/var/www/JARL/keys.json', 'r') as f:
        d = json.load(f)
        client_id = d['DISCORD_OAUTH_CLIENT_ID']
        client_secret = d['DISCORD_OAUTH_CLIENT_SECRET']
        secret = d['SECRET']

    SECRET_KEY = os.environ.get('SECRET_KEY') or secret

    DISCORD_OAUTH_CLIENT_ID = os.environ.get('DISCORD_OAUTH_CLIENT_ID') or client_id
    DISCORD_OAUTH_CLIENT_SECRET = os.environ.get('DISCORD_OAUTH_CLIENT_SECRET') or client_secret
