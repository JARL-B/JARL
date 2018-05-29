from flask import redirect, render_template, request, url_for
from app import app
import os

@app.route('/help')
def help():
    lang = request.args.get('lang') or 'EN'
    lang = lang.upper()

    if 'strings_{}.py'.format(lang) not in os.listdir('../EXT'):
        return redirect(url_for('help'))

    with open('../EXT/strings_{}.py'.format(lang), 'r') as f:
        s = eval(f.read())

    return render_template('help.html', help=s['help_raw'], foot=s['web_foot'], foot2=s['web_foot2'])
