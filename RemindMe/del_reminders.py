import discord
from datetime import datetime

from RemindMe.globalvars import *
from globalvars import restrictions


async def del_reminders(message, client):
    if not isinstance(message.channel, discord.DMChannel):
        if not message.author.guild_permissions.manage_messages:
            scope = message.channel.id
            if scope not in restrictions.keys():
                restrictions[scope] = []
            for role in message.author.roles:
                if role.id in restrictions[scope]:
                    break
            else:
                await message.channel.send(embed=discord.Embed(description='You must be either admin or have a role capable of sending reminders to that channel. Please talk to your server admin, and tell her/him to use the `$restrict` command to specify allowed roles.'))
                return

        li = [ch.id for ch in message.guild.channels] ## get all channels and their ids in the current server
    else:
        li = [message.author.id]

    await message.channel.send('Listing reminders on this server... (be patient, this might take some time)\nAlso, please note the times are done relative to UK time. Thanks.')

    n = 1
    remli = []

    for rem in reminders:
        if rem.channel in li:
            remli.append(rem)
            await message.channel.send('  **' + str(n) + '**: \'' + rem.message + '\' (' + datetime.fromtimestamp(rem.time).strftime('%Y-%m-%d %H:%M:%S') + ')')
            n += 1

    await message.channel.send('List (1,2,3...) the reminders you wish to delete')

    num = await client.wait_for('message', check=lambda m: m.author == message.author and m.channel == message.channel)
    nums = [n.strip() for n in num.content.split(',')]

    dels = 0
    for i in nums:
        try:
            i = int(i) - 1
            if i < 0:
                continue
            item = remli[i]
            reminders.remove(remli[i])
            print('Deleted reminder')
            dels += 1

        except ValueError:
            continue
        except IndexError:
            continue

    await message.channel.send('Deleted {} reminders!'.format(dels))
