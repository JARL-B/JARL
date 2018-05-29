from flask import redirect, render_template, request
from app import app
import json

@app.route('/help')
def help():
    lang = request.args.get('lang') or 'EN'

    with open('../EXT/strings_EN.py', 'r') as f:
        s = eval(f.read())

    return render_template('help.html', help=s['help_raw'])
