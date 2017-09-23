import discord
from discord.ext import commands

import sys, traceback

def get_prefix(bot, msg):
    """A callable Prefix for our bot. This could be edited to allow per server prefixes."""
    
    # Notice how you can use spaces in prefixes. Try to keep them simple though.
    prefixes = ['>?', 'lol ', '!?', 'j.']

    # Check to see if we are outside of a guild. e.g DM's etc.
    if msg.guild.id is None:
        # Only allow ? to be used in DMs
        return '?'

    # If we are in a guild, we allow for the user to mention us or use any of the prefixes in our list.
    return commands.when_mentioned_or(*prefixes)(bot, msg)

# Below cogs represents our folder our cogs are in. Following is the file name. So 'meme.py' in cogs, would be cogs.meme
# Think of it like a dot path import
initial_extensions = ('cogs.simple',
                      'cogs.members',
                      'cogs.owner',
                      'cogs.music',)
                      
bot = commands.Bot(command_prefix=get_prefix, description='Jarl Bot version:0.1')


@bot.event
async def on_ready():
    """The on ready function"""

    print('\n\nLogged in as: {} - {}\nVersion: {}\n'.format(bot.user.name, bot.user.id, discord.__version__))

    # Changes our bots Playing Status. type=1(streaming) for a standard game you could remove type and url.
    await bot.change_presence(game=discord.Game(name='Jarl Bot version 0.1', type=1, url='https://twitch.tv/galacticzytan'))

    # Here we load our extensions listed above in [initial_extensions].
    if __name__ == '__main__':
        for extension in initial_extensions:
            try:
                bot.load_extension(extension)
            except Exception as e:
                print('Failed to load extension {extension}.', file=sys.stderr)
                traceback.print_exc()
    print('Successfully logged in and booted...!')


@bot.command()
async def dm(ctx, member : discord.User, *, message):
   return await member.send(message)
    
bot.run('token', bot=True, reconnect=True)
