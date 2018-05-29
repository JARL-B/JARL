from flask import redirect, render_template, request, url_for
from app import app
import os
import io

base_dir = os.environ.get('BASE_DIR') or '/var/www/JARL/EXT'

@app.route('/')
@app.route('/help')
def help():
    all_langs = sorted([s[-5:-3] for s in os.listdir(base_dir)])
    print(all_langs)

    lang = request.args.get('lang') or 'EN'
    lang = lang.upper()

    if lang not in all_langs:
        return redirect(url_for('help'))

    with io.open('{}/strings_{}.py'.format(base_dir, lang), 'r', encoding='utf8') as f:
        s = eval(f.read())

    return render_template('help.html', help=s['help_raw'], foot=s['web_foot'], foot2=s['web_foot2'], languages=all_langs, footer=s['about'], join=s['join'], invite=s['invite'])
