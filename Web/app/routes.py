from flask import redirect, render_template, request, url_for
from app import app
import os

@app.route('/help')
def help():
    all_langs = sorted([s[-5:-3] for s in os.listdir('../EXT')])

    lang = request.args.get('lang') or 'EN'
    lang = lang.upper()

    if lang not in all_langs:
        return redirect(url_for('help'))

    with open('../EXT/strings_{}.py'.format(lang), 'r') as f:
        s = eval(f.read())

    return render_template('help.html', help=s['help_raw'], foot=s['web_foot'], foot2=s['web_foot2'], languages=all_langs)
