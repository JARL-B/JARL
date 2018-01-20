import time

async def ping(message, client):
  await message.channel.send('Time to receive and process message: {}ms'.format(round((time.time() - message.created_at.timestamp())*1000)))
