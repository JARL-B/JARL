import discord
import json

from TheManagement.globalvars import leave_messages, join_messages

async def servermsg(message, client):
    if isinstance(message.channel, discord.DMChannel):
        return

    if 'leavemsg' in message.content.split(' ')[0]:
        messages = leave_messages
        filen = 'leave'
    else:
        messages = join_messages
        filen = 'join'


    if not message.author.guild_permissions.administrator:
        await message.channel.send('You must be an admin to run this command.')
        return

    if message.guild.id in messages.keys():
        if len(message.content.split(' ')) == 1:
            await message.channel.send('Server {} messages disabled!'.format(filen))
            del messages[message.guild.id]
        else:
            messages[message.guild.id] = [message.content.split(' ',1)[1], message.channel.id]
            await message.channel.send('Server {} messages enabled!'.format(filen))

    else:
        if len(message.content.split(' ')) == 1:
            await message.channel.send('It appears your server doesn\'t yet have a {0} message! To set one, type this command followed by a space, followed by your message. Use two curly braces (`{{}}`) to represent the name of the person who left (we\'ll replace them automatically)'.format(filen))
        else:
            messages[message.guild.id] = [message.content.split(' ',1)[1], message.channel.id]
            await message.channel.send('Server {} messages enabled!'.format(filen))


    with open('DATA/{}_messages.json'.format(filen), 'w') as f:
        json.dump(messages,f)
