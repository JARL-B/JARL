from datetime import datetime

from RemindMe.globalvars import *


async def del_reminders(message, client):
  msgs = [message]

  t = await client.send_message(message.channel, 'Listing reminders on this server... (be patient, this might take some time)\nAlso, please note the times are done relative to UK time. Thanks.')
  msgs.append(t)

  li = [ch.id for ch in message.server.channels] ## get all channels and their ids in the current server

  n = 1
  remli = []

  for inv in intervals:
    if inv[2] in li:
      remli.append(inv)
      t = await client.send_message(message.channel, '  **' + str(n) + '**: \'' + inv[3] + '\' (' + datetime.fromtimestamp(int(inv[0])).strftime('%Y-%m-%d %H:%M:%S') + ')')
      msgs.append(t)
      n += 1

  for rem in calendar:
    if rem[1] in li:
      remli.append(rem)
      t = await client.send_message(message.channel, '  **' + str(n) + '**: \'' + rem[2] + '\' (' + datetime.fromtimestamp(int(rem[0])).strftime('%Y-%m-%d %H:%M:%S') + ')')
      msgs.append(t)
      n += 1

  t = await client.send_message(message.channel, 'List (1,2,3...) the reminders you wish to delete')
  msgs.append(t)

  num = await client.wait_for_message(author=message.author,channel=message.channel)
  msgs.append(num)
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

  msg = await client.send_message(message.channel, 'Deleted {} reminders!'.format(dels))
