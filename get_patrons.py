import discord

from globalvars import *


def get_patrons(level='Patrons'):
  p_server = client.get_guild(350391364896161793)
  p_role = discord.utils.get(p_server.roles,name=level)
  premiums = [user for user in p_server.members if p_role in user.roles]

  return premiums
