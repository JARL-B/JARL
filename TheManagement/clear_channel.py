import asyncio
import discord


async def clear_channel(message,client):
  if not message.author.server_permissions.administrator:
    await client.send_message(message.channel, 'You must be an admin to run this command.')
    return

  await client.send_message(message.channel, 'Please note that this process is very slow on messages older than 14 days.\n**ARE YOU SURE YOU WANT TO CLEAR THIS CHANNEL? (y/N)**')
  t = await client.wait_for_message(author=message.author,channel=message.channel)

  if t.content[0].lower() == 'y':
    total_messages = 4
    delete_slow = False

    while total_messages > 1:
      deletion_chunk = []
      total_messages = 0

      async for message in client.logs_from(channel=message.channel,limit=100):
        if delete_slow:
          await client.delete_message(message)
        else:
          deletion_chunk.append(message)
        total_messages += 1

      try:
        await client.delete_messages(deletion_chunk)

      except:
        delete_slow = True
        for message in deletion_chunk:
          await client.delete_message(message)

    print('performed a full clear')
