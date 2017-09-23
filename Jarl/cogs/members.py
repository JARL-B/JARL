import discord
from discord.ext import commands
import time
import asyncio

class MembersCog:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    async def joined(self, ctx, *, member: discord.Member):
        """Says when a member joined."""
        await ctx.send('{} joined on {}'.format(member.display_name, member.joined_at))

    @commands.command(name='bot')
    async def _bot(self, ctx):
        """Is the bot cool?"""
        await ctx.send('Yes, the bot is cool.')

    @commands.command(name='top_role', aliases=['toprole'])
    @commands.guild_only()
    async def show_toprole(self, ctx, *, member: discord.Member=None):
        """Simple command which shows the members Top Role."""

        if member is None:
            member = ctx.author

        await ctx.send('The top role for {} is {}'.format(member.display_name, member.top_role.name))
    
    @commands.command(name='perms', aliases=['perms_for', 'permissions'])
    @commands.guild_only()
    async def check_permissions(self, ctx, *, member: discord.Member=None):
        """A simple command which checks a members Guild Permissions.
        If member is not provided, the author will be checked."""

        if not member:
            member = ctx.author

        perms = '\n'.join(perm for perm, value in member.guild_permissions if value)

        embed = discord.Embed(title='Permissions for:', description=ctx.guild.name, colour=member.colour)
        embed.set_author(icon_url=member.avatar_url, name=str(member))

        embed.add_field(name='\uFEFF', value=perms)

        await ctx.send(content=None, embed=embed)

    @commands.command(name='ping', aliases=["pong", "speed"])
    async def _checkping(self, ctx):
        '''See if The Bot is Working'''
        pingtime = time.time()
        pingms = await ctx.send("**Timing from <:Jarl:361144681708519424> >> :fast_forward: >> <:discord:361145023129190403> **")
        ping = time.time() - pingtime
        await asyncio.sleep(5)
        await pingms.delete()
        await ctx.send("<:Jarl:361144681708519424> **| The latency is: `%.01f seconds` <:wumpusblob:361145728300613634> **" % ping)


def setup(bot):
    bot.add_cog(MembersCog(bot))
