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
  > `$event <server/me/channel-name/channel-mention> <date-and-time> <message>` - set up an event. Takes times in the format of \[minutes]m[hours]h[days]d[months]/[year]y, for example 0m0h31d12/2018y for 00:00 UTC on the 31st of December 2018.
  > `$interval <time-to-reminder> <interval> [-scope=<channel-name>] <message>` - set up an interval, where the given `message` will be sent every `interval` starting in the given `time-to-reminder`. Takes times in the format of \[num][s/m/h/d]. Ex. `$interval 0s 20m Hello World!` will send `Hello World!` to your channel every 20 minutes. `$interval 0s 20m -scope=other-channel Hello World!` is the same as typing the command in #other-channel..
  > `$notify` - enable/disable personal email reminders for the specific channel.
  > `$todo` - TODO list related commands. Use `$todo help` for proper information.
  > `$todos` - same as `$todo` but for server-wide task management.
  '''
  )

  em2 = discord.Embed(description=
  '''
__TheManagement Commands__
  > `$autoclear [time/s] [channel]` - enables/disables autoclearing, where messages sent to the channel (default your channel) will be automatically deleted after time (default 10 seconds)
  > `$profanity` - enables/disables anti-profanity. Filters many different words and deletes messages containing these words.
  > `$spam` - enables/disables basic anti-spam. Mutes members who send messages too quickly.
  > `$joinmsg [message]` - enables/disables a join message. If no join message is provided, the join message will be disabled. To represent the user joining the server in the join message, use 2 curly braces (`{}`).
  > `$leavemsg [message]` - as above, but for when someone leaves a server.
  > `$tags` - enable/disable the muting of `@everyone` and `@here`. Adds a role which can allow certain users to use the tags. If a user sends a tag, they will receive a discord-wide warning, and upon receiving 4 warnings they will be banned. Immediately bans users who use more than one tag in a message.
  > `$verif` - adds a role called Manager:Email Verified. Upon joining, a user will be required to re-verify their user using an email and a code.
  > `$vote <message>` - call a 10 minute long yes/no vote.

__Other Commands__
  > `$zalgo <msg>` - zalgo-ify some text.
  > `$wiki <search-term>` - search wikipedia for a summary on a term.
  > `$pythagoras a=<num> b=<num> c=<num>` - calculate missing lengths on a right-angled triangle. two of a, b and c must be entered.
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
