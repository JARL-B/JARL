import discord
import asyncio


async def get_help(message,client):
  em = discord.Embed(title='**HELP**',description=
  '''
__Key Commands__
  > `mbprefix <string>` - change the prefix from $ to anything less than 5 characters. This variable is stored on a per-server level. This command does not use a prefix!
  > `$help` - get a PM of this page.
  > `$blacklist <channel-name>` - block or unblock a channel from sending commands. If the bot has sufficient rights, it will also remove any commands in blacklisted channels.

__Reminder Commands__
  > `$del` - delete reminders and intervals on your server.
  > `$remind <server/me> <time-to-reminder> <message>` - set up a reminder. Takes times in the format of \[num][s/m/h/d], for example 10s for 10 seconds, 2s10m for 2 seconds 10 minutes or 10m15s1h2d for 10 minutes, 15 seconds, 1 hour and 2 days.
  > `$event <server/me> <date-and-time> <message>` - set up an event. Takes times in the format of \[minutes]m[hours]h[days]d[months]/[year]y, for example 0m0h31d12/2018y for 00:00 UTC on the 31st of December 2018.
  > `$interval <time-to-reminder> <interval> <message>` - set up an interval, where the given `message` will be sent every `interval` starting in the given `time-to-reminder`. Takes times in the format of \[num][s/m/h/d].
  '''
  )

  em2 = discord.Embed(description=
  '''
__TheManagement Commands__
  > `$clear` - deletes all messages in the current channel. Very slow on old messages.
  > `$autoclear [time/s] [channel]` - enables/disables autoclearing, where messages sent to the channel (default your channel) will be automatically deleted after time (default 10 seconds)
  > `$profanity` - enables/disables anti-profanity. Filters many different words and deletes messages containing these words and various variations on them.
  > `$spam` - enables/disables basic anti-spam. Mutes members who send messages too quickly.
  > `$joinmsg [message]` - enables/disables a join message. If no join message is provided, the join message will be disabled. To represent the user joining the server in the join message, use 2 curly braces (`{}`).
  > `$leavemsg [message]` - as above, but for when someone leaves a server.
  > `$tags` - enable/disable the muting of `@everyone` and `@here`. Adds a role which can allow certain users to use the tags. If a user sends a tag, they will receive a discord-wide warning, and upon receiving 4 warnings they will be banned from the last server they tagged on. Immediately bans users who use more than one tag in a message.
  > `$verif` - adds a role called Manager:Email Verified. Upon joining, a user will be required to re-verify their user using an email and a code.
  > `$vote <message>` - call a 10 minute long yes/no vote.

__Other Commands__
  > `$donate` - view information about donations.

*Do you have a place I can go to get more assistance?*
  Please join our Discord server :)

  https://discord.gg/WQVaYmT
  '''
  )

  await client.send_message(message.channel, embed=em)
  await client.send_message(message.channel, embed=em2)

  await client.add_reaction(message,'📬')
