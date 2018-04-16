import discord
import json

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
        'tags' : {}
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

    for channel, roles in variables[1].items():
        obj = client.get_channel(int(channel))

        if obj is None:
            continue

        if list(filter(lambda x: x['id'] == obj.guild.id, data)):
            list(filter(lambda x: x['id'] == obj.guild.id, data))[0]['autoclears'][obj.id] = time

        else:
            continue

client.run('token')
