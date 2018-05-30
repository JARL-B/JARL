from flask import Flask
from config import Config
from flask_dance import make_discord_blueprint, discord

app = Flask(__name__)
app.config.from_object(Config)
discord_blueprint = make_discord_blueprint(redirect_url='/experimental')
app.register_blueprint(discord_blueprint, url_prefix='/login')

from app import routes
