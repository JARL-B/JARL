import discord
from globalvars import *

def get_patrons(level='Patrons'):
    if patreon:
        p_server = client.get_guild(patreonserver)
        p_role = discord.utils.get(p_server.roles, name=level)
        premiums = [user for user in p_server.members if p_role in user.roles]

        return premiums
    else:
        return client.get_all_members()
