import discord
import asyncio


async def get_help(message,client):
  em = discord.Embed(title='**HELP**',description=
  '''
__Key Commands__
  > `rbprefix <string>` - change the prefix from $ to anything less than 5 characters. This variable is stored on a per-server level. This command does not use a prefix!
  > `$help` - get a PM of this page.
  > `$issue <text>` - send us an issue report.
  > `$blacklist <channel-name>` - block or unblock a channel from sending commands. If the bot has sufficient rights, it will also remove any commands in blacklisted channels.
  > `$del` - delete reminders and intervals on your server.
  > `$bind` - donators donating 5$ or more can bind their donator premium commands to enable a whole server to use premium features. donators donating 8$ can bind to 3 servers. If you bind to another server past this, it will remove the first server you bound to. Binds reset when the bot goes offline, to prevent cheating the donation system.

__Reminder Commands__
  > `$remind <server/me> <time-to-reminder> <message>` - set up a reminder. Takes times in the format of \[num][s/m/h/d], for example 10s for 10 seconds, 2s10m for 2 seconds 10 minutes or 10m15s1h2d for 10 minutes, 15 seconds, 1 hour and 2 days.
  > `$event <server/me> <date-and-time> <message>` - set up an event. Takes times in the format of \[minutes]m[hours]h[days]d[months]/[year]y, for example 0m0h31d12/2018y for 00:00 UTC on the 31st of December 2018.
  > `$interval <time-to-reminder> <interval> <message>` - set up an interval, where the given `message` will be sent every `interval` starting in the given `time-to-reminder`. Takes times in the format of \[num][s/m/h/d].
  '''
  )

  em2 = discord.Embed(description=
  '''
__Other Commands__
  > `$etime` - get the current time in seconds.
  > `$playing <string>` - set the 'Playing' subtext (Superheros only)
  > `$invite <URL>` - invite the bot to another server via URL (has a tendency to not work due to discord bot limitation. Use the link instead: INSERT LINK HERE)
  > `$suggestion <text>` - send us a feature suggestion.
  > `$donate` - view information about donations.
  > `$transport_me` - PROTECT YOURSELF FROM ORANG AND THE VEGETALS.

  **__FAQ__**
*What do I do if I blacklist all the channels?!*
  **__Don't panic!__** No, but seriously don't. Just make another text channel and then use the blacklist command again to un-blacklist (or as some may call, whitelist) the other channels. Simple :)

*What if the prefix gets set to a character that's difficult to access?*
  The `rbprefix` command doesn't require a prefix to access. Therefore, you can always easily change or reset the prefix.

*Why does the help command work even on blacklisted channels?*
  The help command functions on blacklisted channels so that users can still access important information, for example how to un-blacklist a channel.

*Should I use `event` or `remind`?*
  To decide on this, consider: would you use a timer or a calendar to set the reminder? An event accepts a specific date and time as the argument, whereas a remind accepts the amount of time until the reminder, like a stopwatch.

*Do you have a place I can go to get more assistance?*
  Please join our Discord server :)

  https://discord.gg/WQVaYmT
  '''
  )

  await client.send_message(message.channel, embed=em)
  await client.send_message(message.channel, embed=em2)

  await client.add_reaction(message,'📬')
