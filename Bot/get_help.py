## PORTED ##

import discord
import asyncio


async def get_help(message, client):
    em = discord.Embed(title='Help', description='''
__Reminder Commands__
    > `$del` - delete reminders and intervals on your server.
    > `$remind [user/channel] <time-to-reminder> <message>` - set up a reminder. Takes times in the format of [num][s/m/h/d], for example 10s for 10 seconds or 2s10m for 2 seconds 10 minutes. An exact time can be provided as `day`/`month`/`year`-`hour`:`minute`:`second`.
    > `$interval [user/channel] <time-to-reminder> <interval> <message>` - set up an interval, where the given `message` will be sent every `interval` starting in the given `time-to-reminder`. Takes times in the formats above. Ex. `$interval 0s 20m Hello World!` will send `Hello World!` to your channel every 20 minutes.
    > `$todo` - TODO list related commands. Use `$todo help` for more information.
    > `$todos` - same as `$todo` but for server-wide task management.
    > `$timezone` - set your server's timezone, for easier date-based reminders
__TheManagement Commands__
    > `$autoclear [time/s] [channels]` - enables/disables autoclearing, where messages sent to the channel (default your channel) will be automatically deleted after time (default 10 seconds)
    > `$clear <user mentions>` - clears messages made by a user/s
    > `$restrict [role mentions]` - add/remove roles from being allowed to send channel reminders and intervals.
    > `$tag` - Aliasing commands. Use `$tag help` for more information.
    > `$blacklist [channel-name]` - block or unblock a channel from sending commands.

__Other Commands__
    > `$donate` - view information about donations.
    > `mbprefix <string>` - change the prefix from $. This command does not use a prefix!
    > `$info` - get info on the bot.

    > a word surrounded by `<` `>` is a required argument
    > a word surrounded by `[` `]` is an optional argument
    > do not type the brackets when you type out the command! For example, `mbprefix !`, not `mbprefix <!>`

    Please join our Discord server if you need more help

    https://discord.gg/WQVaYmT
    '''
    )

    await message.channel.send(embed=em)

    await message.add_reaction('📬')
