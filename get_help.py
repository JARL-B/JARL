import discord
import asyncio


async def get_help(message,client):
  em = discord.Embed(title='**HELP**',description=
  '''
__Key Commands__
  > `mbprefix <string>` - change the prefix from $ to anything less than 5 characters. This variable is stored on a per-server level. This command does not use a prefix!
  > `$help` - get a PM of this page.
  > `$blacklist [channel-name]` - block or unblock a channel from sending commands. If the bot has sufficient rights, it will also remove any commands in blacklisted channels.

__Reminder Commands__
  > `$del` - delete reminders and intervals on your server.
  > `$remind <server/me/channel-name/channel-mention> <time-to-reminder> <message>` - set up a reminder. Takes times in the format of \[num][s/m/h/d], for example 10s for 10 seconds, 2s10m for 2 seconds 10 minutes or 10m15s1h2d for 10 minutes, 15 seconds, 1 hour and 2 days.
  > `$interval <time-to-reminder> <interval> [-scope=<channel-name>] <message>` - set up an interval, where the given `message` will be sent every `interval` starting in the given `time-to-reminder`. Takes times in the format of \[num][s/m/h/d]. Ex. `$interval 0s 20m Hello World!` will send `Hello World!` to your channel every 20 minutes. `$interval 0s 20m -scope=other-channel Hello World!` is the same as typing the command in #other-channel..
  > `$todo` - TODO list related commands. Use `$todo help` for proper information.
  > `$todos` - same as `$todo` but for server-wide task management.
  '''
  )

  em2 = discord.Embed(description=
  '''
__TheManagement Commands__
  > `$autoclear [time/s] [channel]` - enables/disables autoclearing, where messages sent to the channel (default your channel) will be automatically deleted after time (default 10 seconds)
  > `$clear <user mentions>` - clears messages made by a user/s. Clears up to 100 messages up to 14 days old (sorry, Discord limitations)
  > `$spam` - enables/disables basic anti-spam. Mutes members who send messages too quickly.
  > `$joinmsg [message]` - enables/disables a join message. If no join message is provided, the join message will be disabled. To represent the user joining the server in the join message, use 2 curly braces (`{}`).
  > `$leavemsg [message]` - as above, but for when someone leaves a server.
  > `$terms` - enable custom term filtering. Use `$terms show` to list all filters and `$terms [word]` to add to the list.

__Other Commands__
  > `$donate` - view information about donations.

  '''
  )

  em3 = discord.Embed(title='**HELP**', description='''

__Help help__
  > a word surrounded by `<` `>` is a required argument
  > a word surrounded by `[` `]` is an optional argument
  > if there is a `/` in the argument name, this means you can choose between different things
  > do not type the brackets when you type out the command! For example, `mbprefix !`, not `mbprefix <!>`
  > if an argument looks like this: `[-scope=<channel>]`, it is optional and requires you to type `-scope=` to use. For example, `-scope=my-channel-name`.

*Do you have a place I can go to get more assistance?*
  Please join our Discord server :)

  https://discord.gg/WQVaYmT
  '''
  )

  await client.send_message(message.channel, embed=em)
  await client.send_message(message.channel, embed=em2)
  await client.send_message(message.channel, embed=em3)

  await client.add_reaction(message,'📬')
