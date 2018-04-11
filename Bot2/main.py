from server_data import ServerData
from sloccount import sloccount_py

import discord
import msgpack
import pytz

import zlib
import datetime
import time
import sys
import os

class BotClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super(BotClient, self).__init__(*args, **kwargs)
        self.get_server = lambda x: [d for d in self.data if d.id == x.id][0]

        self.data = []
        self.DEFAULT_PREFIX = '$'

        self.commands = {
            'help' : self.help,
            'info' : self.info,
            'donate' : self.donate,

            'prefix' : self.change_prefix,

            'timezone' : self.timezone
        }

        self.strings = {
            'help' : 'NULL'
        }

        self.template = {
            'id' : 0,
            'prefix' : self.DEFAULT_PREFIX,
            'timezone' : 'UTC',
            'autoclear' : {},
            'blacklist' : []
        }

        try:
            with open('data.msgpack.zlib', 'rb') as f:
                for d in msgpack.unpackb(zlib.decompress(f.read()), encoding='utf8'):
                    self.validate_data(d)
                    self.data.append(ServerData(**d))
        except FileNotFoundError:
            pass

        try:
            open('strings.py', 'r').close()
        except FileNotFoundError:
            print('Strings file not present. Exiting...')
            sys.exit()


    def validate_data(self, d):
        for key, default in self.template.items():
            if key not in d.keys():
                d[key] = default


    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------------')
        await client.change_presence(activity=discord.Game(name='@{} help'.format(self.user.name)))


    async def on_guild_remove(self, guild):
        self.data = [d for d in self.data if d.id != guild.id]


    async def on_message(self, message):

        if isinstance(message.channel, discord.DMChannel) or message.author.bot or message.content == None:
            return

        if len([d for d in self.data if d.id == message.guild.id]) == 0:
            s = ServerData(**self.template)
            s.id = message.guild.id

            self.data.append(s)

        with open('strings.py', 'r') as f:
            self.strings = eval(f.read())

        if await self.get_cmd(message):
            with open('data.msgpack.zlib', 'wb') as f:
                f.write(zlib.compress(msgpack.packb([d.__dict__ for d in self.data])))


    async def get_cmd(self, message):

        server = self.get_server(message.guild)
        prefix = server.prefix

        if message.content[0:len(prefix)] == prefix:
            command = (message.content + ' ')[len(prefix):message.content.find(' ')]
            if command in self.commands:
                stripped = (message.content + ' ')[message.content.find(' '):].strip()
                await self.commands[command](message, stripped, server)
                return True

        elif self.user.id in map(lambda x: x.id, message.mentions) and len(message.content.split(' ')) > 1:
            if message.content.split(' ')[1] in self.commands.keys():
                stripped = (message.content + ' ').split(' ', 2)[-1].strip()
                await self.commands[message.content.split(' ')[1]](message, stripped, server)
                return True

        return False


    async def change_prefix(self, message, stripped, server):
        if stripped:
            stripped += ' '
            server.prefix = stripped[:stripped.find(' ')]
            await message.channel.send(self.strings['prefix']['success'].format(prefix=server.prefix))

        else:
            await message.channel.send(self.strings['prefix']['no_argument'].format(prefix=server.prefix))


    async def help(self, message, *args):
        embed = discord.Embed(description=self.strings['help'])
        await message.channel.send(embed=embed)


    async def info(self, message, stripped, server):
        embed = discord.Embed(description=self.strings['info'].format(prefix=server.prefix, sloc=sloccount_py(), user=self.user.name))
        await message.channel.send(embed=embed)


    async def donate(self, message, stripped, server):
        embed = discord.Embed(description=self.strings['donate'])
        await message.channel.send(embed=embed)


    async def timezone(self, message, stripped, server):
        if stripped == '':
            await message.channel.send(embed=discord.Embed(description=self.strings['timezone']['no_argument'].format(prefix=server.prefix, timezone=server.timezone)))

        else:
            if stripped not in pytz.all_timezones:
                await message.channel.send(embed=discord.Embed(description=self.strings['timezone']['no_timezone']))
            else:
                server.timezone = stripped
                d = datetime.datetime.now(pytz.timezone(server.timezone))

                await message.channel.send(embed=discord.Embed(description=self.strings['timezone']['success'].format(timezone=server.timezone, time=d.strftime('%H:%M:%S'))))


    async def remind(self, message, stripped, server):

    async def interval(self, message, stripped, server):

    async def autoclear(self, message, stripped, server):

    async def blacklist(self, message, stripped, server):

    async def clear(self, message, stripped, server):

    async def restrict(self, message, stripped, server):

    async def tag(self, message, stripped, server):

    async def todo(self, message, stripped, server):

    async def delete(self, message, stripped, server):



try: ## token grabbing code
    with open('token','r') as token_f:
        token = token_f.read().strip('\n')

except:
    print('no token provided')
    sys.exit(-1)

client = BotClient()
client.run(token)
