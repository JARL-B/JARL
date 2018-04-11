{
    'admin_required' : 'You need to be an admin to run this command',

    'help' : '''
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
''',

    'info' : '''
Default prefix: `$`
Reset prefix: `@{user} prefix $`
Help: `{prefix}help`

**Welcome to RemindMe!**
Developer: <@203532103185465344>
Cool guy who knows what he's on about: <@174243954487853056>
Icon: <@253202252821430272>
Find me on https://discord.gg/WQVaYmT and on https://github.com/JellyWX :)

Framework: `discord.py`
Total SᵒᵘʳᶜᵉLᶦⁿᵉˢOᶠCᵒᵈᵉ: {sloc} (100% Python)
Hosting provider: OVH

My other bot (Patron only):
https://discordapp.com/oauth2/authorize?client_id=411224415863570434&scope=bot&permissions=35840

*If you have enquiries about new features, please send to the discord server*
*If you have enquiries about bot development for you or your server, please DM me*
''',

    'donate' : '''
Thinking of adding a monthly contribution? Press below for my patreon and official bot server :D
https://www.patreon.com/jellywx

https://discord.gg/WQVaYmT

Here's some more information:

When you donate, Patreon will automatically rank you up on our Discord server, supposing you have properly linked your Patreon and Discord accounts!
With your new rank, you'll be able to:
: use Patron-only commands like `interval`
: set more reminders (unlimited)
: set longer reminders (2000 chars)
: set more/longer tags
: use the Patron-only `TrackerBot` with your server to track your game time through Discord

Anyone who is a Patron, thank you :D You make this bot sustainable

Please note, you must be connected to the Discord server to receive Patreon rewards.
''',

    'prefix' : {
        'no_argument' : '''
Please use this command as `{prefix}prefix <prefix>`
''',
        'success' : '''
Prefix changed to {prefix}
'''
    },

    'timezone' : {

        'no_argument' : '''
Usage:
    ```{prefix}timezone <Name>```
Example:
    ```{prefix}timezone Europe/London```
All timezones: https://gist.github.com/heyalexej/8bf688fd67d7199be4a1682b3eec7568
Current timezone: {timezone}''',

        'no_timezone' : '''Timezone not recognized. A list is available at https://gist.github.com/heyalexej/8bf688fd67d7199be4a1682b3eec7568''',

        'success' : '''Timezone has been set to {timezone}. Your current time should be {time}'''
    },

    'restrict' : {

        'disabled' : '''Disabled channel reminder permissions for roles.''',

        'enabled' : '''Enabled channel reminder permissions for roles.''',

        'allowed' : 'Allowed roles: {}'
    },

    'clear' : {

        'no_argument' : '''Please mention users you wish to remove messages of.'''

    },

    'remind' : {
        'no_argument' : '''
Usage:
    ```$remind [channel mention or user mention] <time to or time at> <message>```
Example:
    ```$remind #general 10s Hello world```
    ```$remind 10:30 It\'s now 10:30```'''
    },

}
