import discord
from datetime import datetime
import time

from globalvars import timezones

async def timezone(message, client):
  if not message.author.guild_permissions.administrator:
    await message.channel.send(embed=discord.Embed(description='You must be an admin to use this command`'))
    return

  contents = message.content.split(' ')

  if len(contents) != 2 or len(contents[1].split(':')) > 2:
    await message.channel.send(embed=discord.Embed(description='Usage: `$timezone <hours from UTC>`'))

  else:
    contents.pop(0)
    time_units = contents[0]

    total_time_delta = int(time_units) * 3600

    timezones[message.guild.id] = total_time_delta

    a = datetime.fromtimestamp(time.time() + total_time_delta)

    await message.channel.send(embed=discord.Embed(description='Timezone set. Your current time should be {}:{}'.format(a.hour, a.minute)))
