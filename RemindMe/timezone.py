import discord
from datetime import datetime
import time
import json

from RemindMe.globalvars import timezones

async def timezone(message, client):
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
      if time_units.upper() == 'EST':
        await message.channel.send(embed=discord.Embed(description='If you\'re in America, please use EDT or UEDT rather than EST (EST is also Ekaterinburg Standard Time, UTC+6)'))
      with open('EXT/timezones.json', 'r') as f:
        tzs = json.load(f)
        if time_units.upper() in tzs.keys():
          total_time_delta = tzs[time_units.upper()] * 3600
        else:
          await message.channel.send(embed=discord.Embed(description='Sorry, that timezone isn\'t recognized. Please use a 3/4 letter code or a single negative or positive number.'))
          return

    timezones[message.guild.id] = total_time_delta

    a = datetime.fromtimestamp(time.time() + total_time_delta)

    await message.channel.send(embed=discord.Embed(description='Timezone set. Your current time should be {}:{}. Please note that in some cases (particularly around UTC midnight), you may have to specify the day you wish the reminder to occur on. **If the time is wrong, it may be because of Daylight Saving Time. Please set manually if this is the case**'.format(a.hour, a.minute)))

  with open('DATA/timezones.json','w') as f:
    json.dump(timezones, f)
