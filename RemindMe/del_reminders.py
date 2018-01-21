from datetime import datetime

from RemindMe.globalvars import *

from globalvars import restrictions

async def del_reminders(message, client):
  if not message.author.guild_permissions.administrator:
    if scope not in restrictions.keys():
      restrictions[scope] = []
    for role in message.author.roles:
      if role.id in restrictions[scope]:
        break
    else:
      await message.channel.send(embed=discord.Embed(description='You must be either admin or have a role capable of sending reminders to that channel. Please talk to your server admin, and tell her/him to use the `$restrict` command to specify allowed roles.'))
      return

  await message.channel.send('Listing reminders on this server... (be patient, this might take some time)\nAlso, please note the times are done relative to UK time. Thanks.')

  li = [ch.id for ch in message.guild.channels] ## get all channels and their ids in the current server

  n = 1
  remli = []

  for inv in intervals:
    if inv[2] in li:
      remli.append(inv)
      await message.channel.send('  **' + str(n) + '**: \'' + inv[3] + '\' (' + datetime.fromtimestamp(int(inv[0])).strftime('%Y-%m-%d %H:%M:%S') + ')')
      n += 1

  for rem in calendar:
    if rem[1] in li:
      remli.append(rem)
      await message.channel.send('  **' + str(n) + '**: \'' + rem[2] + '\' (' + datetime.fromtimestamp(int(rem[0])).strftime('%Y-%m-%d %H:%M:%S') + ')')
      n += 1

  await message.channel.send('List (1,2,3...) the reminders you wish to delete')

  num = await client.wait_for('message', check=lambda m: m.author == message.author and m.channel == message.channel)
  nums = num.content.split(',')

  dels = 0
  for i in nums:
    try:
      i = int(i) - 1
      if i < 0:
        continue
      item = remli[i]
      if item in intervals:
        intervals.remove(remli[i])
        print('Deleted interval')
        dels += 1

      else:
        calendar.remove(remli[i])
        print('Deleted reminder')
        dels += 1

    except ValueError:
      continue
    except IndexError:
      continue

  await message.channel.send('Deleted {} reminders!'.format(dels))
