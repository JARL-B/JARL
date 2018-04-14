import discord

client = discord.Client()
files = ['blacklist.json', 'autoclears.json', 'restrictions.json', 'tags.json', 'prefix.json']



@client.event
def on_ready():


client.run(token)
