import asyncio
import time

async def clear_by(message, client):
  if not message.author.guild_permissions.administrator:
    await message.channel.send('You must be an admin to run this command.')
    return

  if len(message.mentions) == 0:
    await message.channel.send('Please mention users you wish to remove messages of.')
    return

  delete_list = []

  async for m in message.channel.history(limit=1000):
    if time.time() - m.created_at.timestamp() >= 1209600 or len(delete_list) > 99:
      break

    if m.author in message.mentions:
      delete_list.append(m)

  await message.channel.delete_messages(delete_list)
