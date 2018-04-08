import discord
from datetime import datetime
import time
import json
import pytz

from RemindMe.globalvars import timezones

async def timezone(message, client):
    if isinstance(message.channel, discord.DMChannel):
        return

    if not message.author.guild_permissions.administrator:
        await message.channel.send(embed=discord.Embed(description='You must be an admin to use this command`'))
        return

    contents = message.content.split(' ')

    if len(contents) != 2 or len(contents[1].split(':')) > 2:
        if message.guild.id in timezones.keys():
            a = datetime.fromtimestamp(time.time() + timezones[message.guild.id])
            await message.channel.send(embed=discord.Embed(description='Usage: `$timezone <hours from UTC>`. Your current time should be {}:{}'.format(a.hour, a.minute)))
            return
        await message.channel.send(embed=discord.Embed(description='Usage: `$timezone <hours from UTC>`'))

    else:
        contents.pop(0)
        time_units = contents[0]

        try:
            total_time_delta = int(time_units) * 3600
        except ValueError:
            try:
                t = datetime.now(pytz.timezone(time_units)).strftime('%z')
                minutes = int(t[-2:])
                hours = int(t[:-2])

                total_time_delta = (hours * 3600) + (minutes * 60)

            except pytz.exceptions.UnknownTimeZoneError:
                await message.channel.send(embed=discord.Embed(description='Timezone not recognized. Please find a list of timezones at https://gist.github.com/heyalexej/8bf688fd67d7199be4a1682b3eec7568. DST is automatically accounted for.'))
                return

        timezones[message.guild.id] = total_time_delta

        a = datetime.utcfromtimestamp(time.time() + total_time_delta)

        await message.channel.send(embed=discord.Embed(description='Timezone set. Your current time should be {}:{}. Please note that in some cases (particularly around UTC midnight), you may have to specify the day you wish the reminder to occur on. **If the time is wrong, it may be because of Daylight Saving Time. Please set manually if this is the case**'.format(a.hour, a.minute)))

    with open('DATA/timezones.json','w') as f:
        json.dump(timezones, f)
