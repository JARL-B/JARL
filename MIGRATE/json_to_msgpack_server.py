import discord
import json
import configparser
import msgpack
import zlib
import sys

files = ['blacklist.json', 'autoclears.json', 'restrictions.json', 'tags.json', 'prefix.json']
directory = 'DATA'
default_prefix = '$'

client = discord.Client()

variables = [None, None, None, None, None]


@client.event
async def on_ready():
    print('Online now! Beginning conversion...')
    for x in range(len(files)):
        with open('{}/{}'.format(directory, files[x]), 'r') as f:
            variables[x] = json.load(f)

    template = {
        'id' : 0,
        'prefix' : default_prefix,
        'timezone' : 'UTC',
        'autoclears' : {},
        'blacklist' : [],
        'restrictions' : [],
        'tags' : {},
        'language' : 'EN'
    }

    data = []

    for g in client.guilds:
        new = template.copy()

        new['id'] = g.id
        data.append(new)

    for channel in variables[0]:
        obj = client.get_channel(int(channel))

        if obj is None:
            continue

        if list(filter(lambda x: x['id'] == obj.guild.id, data)):
            list(filter(lambda x: x['id'] == obj.guild.id, data))[0]['blacklist'].append(obj.id)

        else:
            continue

    for channel, time in variables[1].items():
        obj = client.get_channel(int(channel))

        if obj is None:
            continue

        if list(filter(lambda x: x['id'] == obj.guild.id, data)):
            list(filter(lambda x: x['id'] == obj.guild.id, data))[0]['autoclears'][obj.id] = time

        else:
            continue

    for channel, roles in variables[2].items():
        obj = client.get_channel(int(channel))

        if obj is None:
            continue

        if list(filter(lambda x: x['id'] == obj.guild.id, data)):
            list(filter(lambda x: x['id'] == obj.guild.id, data))[0]['restrictions'] += roles

        else:
            continue

    for guild, tags in variables[3].items():
        obj = client.get_guild(int(guild))

        if list(filter(lambda x: x['id'] == obj.id, data)):
            list(filter(lambda x: x['id'] == obj.id, data))[0]['tags'] = tags

    for guild, prefix in variables[4].items():
        obj = client.get_guild(int(guild))

        if list(filter(lambda x: x['id'] == obj.id, data)):
            list(filter(lambda x: x['id'] == obj.id, data))[0]['prefix'] = prefix

    print(data)

    with open('{}/data.msgpack.zlib'.format(directory), 'wb') as f:
        f.write(zlib.compress(msgpack.packb(data)))

    sys.exit()

config = configparser.SafeConfigParser()
config.read('config.ini')

client.run(config.get('DEFAULT', 'token'))
