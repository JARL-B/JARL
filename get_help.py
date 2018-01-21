## PORTED ##

import discord
import asyncio


async def get_help(message, client):
  em = discord.Embed(title='**HELP**',description=
  '''
__Key Commands__
  > `mbprefix <string>` - change the prefix from $ to anything less than 5 characters. This variable is stored on a per-server level. This command does not use a prefix!
  > `$help` - get this page.
  > `$info` - get info on the bot.
  > `$blacklist [channel-name]` - block or unblock a channel from sending commands. If the bot has sufficient rights, it will also remove any commands in blacklisted channels.

__Reminder Commands__
  > `$del` - delete reminders and intervals on your server.
  > `$remind [user/channel] <time-to-reminder> <message>` - set up a reminder. Takes times in the format of [num][s/m/h/d], for example 10s for 10 seconds or 2s10m for 2 seconds 10 minutes. An exact time can be provided as `day`/`month`/`year`-`hour`:`minute`:`second`.
  > `$interval [user/channel] <time-to-reminder> <interval> <message>` - set up an interval, where the given `message` will be sent every `interval` starting in the given `time-to-reminder`. Takes times in the formats above. Ex. `$interval 0s 20m Hello World!` will send `Hello World!` to your channel every 20 minutes.
  > `$todo` - TODO list related commands. Use `$todo help` for proper information.
  > `$todos` - same as `$todo` but for server-wide task management.
  > `timezone` - set your server's timezone, for easier date-based reminders (experimental)
  '''
  )

  em2 = discord.Embed(title='**HELP**', description='''
__TheManagement Commands__
  > `$autoclear [time/s] [channels]` - enables/disables autoclearing, where messages sent to the channel (default your channel) will be automatically deleted after time (default 10 seconds)
  > `$clear <user mentions>` - clears messages made by a user/s. Clears up to 100 messages up to 14 days old (sorry, Discord limitations)
  > `$spam` - enables/disables basic anti-spam. Mutes members who send messages too quickly.
  > `$joinmsg [message]` - enables/disables a join message. If no join message is provided, the join message will be disabled. To represent the user joining the server in the join message, use 2 curly braces (`{}`).
  > `$leavemsg [message]` - as above, but for when someone leaves a server.
  > `$restrict [role mentions]` - add/remove roles from being allowed to send channel reminders and intervals.

__Other Commands__
  > `$donate` - view information about donations.

  > a word surrounded by `<` `>` is a required argument
  > a word surrounded by `[` `]` is an optional argument
  > do not type the brackets when you type out the command! For example, `mbprefix !`, not `mbprefix <!>`

*Do you have a place I can go to get more assistance?*
  Please join our Discord server :)

  https://discord.gg/WQVaYmT
  '''
  )

  await message.channel.send(embed=em)
  await message.channel.send(embed=em2)

  await message.add_reaction('📬')
