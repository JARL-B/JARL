import discord

from globalvars import prefix

async def info(message, client):
  if message.guild.id in prefix.keys():
    pref = prefix[message.guild.id]
  else:
    pref = '$'

  em = discord.Embed(title='**INFO**',description=
  '''
  Default prefix: `$`
  Reset prefix: `mbprefix $`
  Help: `{}help`

  **Welcome to RemindMe!**
  Developer: <@203532103185465344>
  Cool guy who knows what he's on about: <@174243954487853056>
  Icon: <@253202252821430272>
  Find me on https://discord.gg/WQVaYmT and on https://github.com/JellyWX :)

  Framework: `discord.py`
  Total SLOC: 939 (100% Python) (stats generated using David A. Wheeler's 'SLOCCount')
  Hosting provider: OVH

  *If you have enquiries about new features, please send to the discord server*
  *If you have enquiries about bot development for you or your server, please DM me*

  **Check out this bot too, if you need some eye bleach :)**
  https://discordapp.com/api/oauth2/authorize?client_id=399237341652320278&permissions=0&scope=bot
  '''.format(pref)
  )

  await message.channel.send(embed=em)

  await message.add_reaction('📬')
