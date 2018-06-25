from flask import redirect, render_template, request, url_for, session
from app import app, discord
import os
import io
import requests
import sqlite3
import json
from datetime import datetime

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

        for index in range(len(session.get('reminders'))):
            try:
                reminder_rewrite = [x for x in session.get('reminders') if x['index'] == index][0]
            except IndexError:
                return '400 Bad Request'

            if request.form.get('delete{}'.format(index)) is not None:

                with sqlite3.connect(base_dir + 'DATA/calendar.db') as connection:
                    cursor = connection.cursor()

                    cursor.execute('DELETE FROM reminders WHERE channel = ? AND message = ? AND time = ?', (reminder_rewrite['channel']['id'], reminder_rewrite['message'], reminder_rewrite['time'][0]))

            elif request.form.get('message{}'.format(index)) != reminder_rewrite['message']:

                with sqlite3.connect(base_dir + 'DATA/calendar.db') as connection:
                    cursor = connection.cursor()

                    cursor.execute('UPDATE reminders SET message = ? WHERE channel = ? AND message = ? AND time = ?', (request.form.get('message{}'.format(index)), reminder_rewrite['channel']['id'], reminder_rewrite['message'], reminder_rewrite['time'][0]))


        try:
            session.pop('reminders')
        except KeyError:
            pass

        return redirect(url_for('dashboard', id=request.args.get('id')))

    else:
        reminders = []

        if request.args.get('refresh') == '1':
            session.pop('guilds')
            return redirect(url_for('dashboard'))

        if session.get('guilds') is None: # the code below is time-consuming; only run on first load and if the user wants to refresh the guild list.

            user = discord.get('api/users/@me').json()
            guilds = discord.get('api/users/@me/guilds').json()

            user_id = user['id']

            available_guilds = []

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

                    elif (guild['permissions'] & 0x00002000) or (guild['permissions'] & 0x00000020) or (guild['permissions'] & 0x00000008):
                        available_guilds.append(guild)
                        continue

                    elif json.loads(dict(restrictions)['restrictions']) == []:
                        continue

                    member = requests.get('https://discordapp.com/api/v6/guilds/{}/members/{}'.format(idx, user_id), headers={'Authorization': 'Bot {}'.format(app.config['BOT_TOKEN'])}).json()
                    for role in member['roles']:
                        if int(role) in json.loads(dict(restrictions)['restrictions']):
                            available_guilds.append(guild)
                            break

            session['guilds'] = available_guilds

        if request.args.get('id') is not None:
            for guild in session['guilds']:
                if guild['id'] == request.args.get('id'):
                    channels = requests.get('https://discordapp.com/api/v6/guilds/{}/channels'.format(guild['id']), headers={'Authorization': 'Bot {}'.format(app.config['BOT_TOKEN'])}).json()
                    break

            else:
                return '403. Don\'t be naughty.'

            with sqlite3.connect(base_dir + '/DATA/calendar.db') as connection:
                cursor = connection.cursor()
                cursor.row_factory = sqlite3.Row

                command = 'SELECT * FROM reminders WHERE channel IN ({})'.format(','.join(['?'] * len(channels)))
                cursor.execute(command, [int(x['id']) for x in channels])

                reminders = [dict(x) for x in cursor.fetchall()]

            index = 0

            for reminder in reminders:
                reminder['index'] = index
                index += 1

                channel = [x for x in channels if int(x['id']) == reminder['channel']][0]

                reminder['channel'] = channel

                reminder['time'] = [reminder['time'], datetime.fromtimestamp(reminder['time']).strftime('%d/%b/%Y %H:%M:%S')]

        session['reminders'] = reminders

        return render_template('dashboard.html', guilds=session['guilds'], reminders=session['reminders'])
