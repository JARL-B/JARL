from flask import redirect, render_template, request, url_for, session
from app import app, discord
import os
import io
import requests
import sqlite3
import json

base_dir = os.environ.get('BASE_DIR') or '../'

@app.route('/')
@app.route('/help')
def help():
    all_langs = sorted([s[-5:-3] for s in os.listdir(base_dir + 'EXT')])
    print(all_langs)

    lang = request.args.get('lang') or 'EN'
    lang = lang.upper()

    if lang not in all_langs:
        return redirect(url_for('help'))

    with io.open('{}EXT/strings_{}.py'.format(base_dir, lang), 'r', encoding='utf8') as f:
        s = eval(f.read())

    return render_template('help.html', help=s['help_raw'], foot=s['web_foot'], foot2=s['web_foot2'], languages=all_langs, footer=s['about'], join=s['join'], invite=s['invite'])


@app.route('/oauth')
def oauth():
    if not discord.authorized:
        return redirect(url_for('discord.login'))

    return redirect(url_for('dashboard'))


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if not discord.authorized:
        return redirect(url_for('oauth'))

    if request.method == 'POST':
        pass # make DB modifications & check user auth.

    elif request.method == 'GET':
        if request.args.get('refresh') == '1':
            session.pop('guilds')
            session.pop('guild_names')
            return redirect(url_for('dashboard'))

        if session.get('guilds') is not None and session.get('guild_names') is not None:
            pass

        else:

            user = discord.get('api/users/@me').json()
            guilds = discord.get('api/users/@me/guilds').json()

            user_id = user['id']

            available_guilds = []
            guild_ids = []

            with sqlite3.connect(base_dir + '/DATA/calendar.db') as connection:
                cursor = connection.cursor()
                cursor.row_factory = sqlite3.Row

                for guild in guilds:
                    idx = guild['id']

                    command = 'SELECT restrictions FROM servers WHERE id = ?'
                    cursor.execute(command, (idx,))

                    restrictions = cursor.fetchone()

                    if restrictions is None:
                        continue

                    member = requests.get('https://discordapp.com/api/v6/guilds/{}/members/{}'.format(idx, user_id), headers={'authorization': 'Bot {}'.format(app.config['BOT_TOKEN'])}).json()
                    for role in member['roles']:
                        if int(role) in json.loads(dict(restrictions)['restrictions']):
                            available_guilds.append(guild['name'])
                            guild_ids.append(guild['id'])
                            break

            session['guilds'] = guild_ids
            session['guild_names'] = available_guilds

        return render_template('dashboard.html', guilds=session['guild_names'])

@app.route('/dash_help')
def dashboard_help():
    return render_template('dashboard_help.html')
