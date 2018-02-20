import discord

async def ffs(message, client):
  f = open('EXT/ffs.gif', 'rb')
  await message.channel.send(file=discord.File(f, 'ffs.gif'))
  f.close()
