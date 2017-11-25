import time

async def ping(message,client):
  await client.send_message(message.channel, 'Time to receive and process message: {}ms'.format(round((time.time() - message.timestamp.timestamp())*1000)))
