from flask import redirect, render_template, request
from app import app
import json

@app.route('/help')
def help():
    lang = request.args.get('lang') or 'EN'
    
