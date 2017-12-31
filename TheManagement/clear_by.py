import asyncio
import time

async def clear_by(message, client):
  if not message.author.server_permissions.administrator:
    await client.send_message(message.channel, 'You must be an admin to run this command.')
    return

  if len(message.mentions) == 0:
    await client.send_message(message.channel, 'Please mention users you wish to remove messages of.')
    return

  delete_list = []

  async for m in client.logs_from(message.channel, limit=1000):
    if time.time() - m.timestamp.timestamp() >= 1209600 or len(delete_list) > 99:
      break

    if m.author in message.mentions:
      delete_list.append(m)

  await client.delete_messages(delete_list)
