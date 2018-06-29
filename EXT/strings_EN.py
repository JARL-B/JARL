#: english

{
    'blacklisted' : ''':x: This channel is blacklisted :x:''',

    'admin_required' : 'You need to be an admin to run this command.',

    'help' : '''Please visit https://jellywx.co.uk/help?lang=EN''',

    'help_raw' : [
        ['''Reminder Commands''', {
            '$del' : 'delete reminders and intervals on your server. If the reminders are set up for DMs, direct message this command to the bot.',

            '$remind [user/channel] <time-to-reminder> <message>' : 'set up a reminder. Takes times in the format of [num][s/m/h/d], for example 10s for 10 seconds or 2s10m for 2 seconds 10 minutes. An exact time can be provided as `day`/`month`/`year`-`hour`:`minute`:`second`.',

            '$interval [user/channel] <time-to-reminder> <interval> <message>' : 'set up an interval, where the given `message` will be sent every `interval` starting in the given `time-to-reminder`. Takes times in the formats above. Ex. `$interval 0s 20m Hello World!` will send `Hello World!` to your channel every 20 minutes.',

            '$todo' : 'TODO list related commands. Use `$todo help` for more information.',

            '$todos' : 'same as `$todo` but for server-wide task management.',

            '$timezone' : 'set your server\'s timezone, for easier date-based reminders.' }],

        ['''Management Commands''', {
            '$autoclear [time/s] [channels]' : 'enables/disables autoclearing, where messages sent to the channel (default your channel) will be automatically deleted after time (default 10 seconds).',

            '$clear <user mentions>' : 'clears messages made by a user/s.',

            '$restrict [role mentions]' : 'add/remove roles from being allowed to send channel reminders and intervals.',

            '$tag' : 'Aliasing commands. Use `$tag help` for more information.',

            '$blacklist [channel-name]' : 'block or unblock a channel from sending commands.' }],

        ['''Other Commands''', {
            '$donate' : 'view information about donations.',

            'mbprefix <string>' : 'change the prefix from $. This command does not use a prefix!',

            '$info' : 'get info on the bot.',

            '$lang <name>' : 'change the language.',

            '$clock [12]' : 'get the current time, optionally as 12 hour clock.' }
        ]
    ],

    'web_foot_title' : 'Extra Information',
    'web_foot' : 'Do not type the brackets when you type out the command! For example, mbprefix !, not mbprefix <!>',
    'web_foot2' : 'Please join our Discord Support Server if you need more help:',

    'about' : {'About' : ['Bot Created By: Jude Southworth', 'Github: <a href=https://github.com/JellyWX>https://github.com/JellyWX</a>', 'Want a bot making? Please contact me on Discord.', 'Hosting provider: OVH']},

    'join' : 'Join our Discord Server',
    'invite' : 'Invite the Bot',

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

Anyone who is a Patron, thank you :D You make this bot sustainable

Please note, you must be connected to the Discord server to receive Patreon rewards.
''',

    'prefix' : {
        'no_argument' : '''
Please use this command as `mbprefix <prefix>`
''',
        'success' : '''
Prefix changed to {prefix}
''',

        'too_long' : '''Please select a prefix under 5 characters'''
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

        'allowed' : '''Allowed roles: {}'''
    },

    'clear' : {

        'no_argument' : '''Please mention users you wish to remove messages of.'''

    },

    'remind' : {
        'no_argument' : '''
Usage:
    ```{prefix}remind [channel mention or user mention] <time to or time at> <message>```
Example:
    ```{prefix}remind #general 10s Hello world```
    ```{prefix}remind 10:30 It\'s now 10:30```''',

        'invalid_tag' : '''Couldn't find a location by your tag present.''',

        'invalid_time' : '''Make sure the time you have provided is in the format of [num][s/m/h/d][num][s/m/h/d] etc. or `day/month/year-hour:minute:second`.''',

        'invalid_count' : '''Too many reminders in specified channel! Use `{prefix}del` to delete some of them, or use `{prefix}donate` to increase your maximum ($5 tier).''',

        'invalid_chars' : '''Reminder message too long! (max 150, you used {}). Use `{prefix}donate` to increase your character limit to 1900 ($5 tier).''',

        'invalid_chars_2000' : '''Discord restrictions mean we can\'t send reminders 2000+ characters. Sorry.''',

        'no_perms' : '''You must have `Manage Messages` or have a role capable of sending reminders to that channel. Please talk to your server admin, and tell her/him to use the `{prefix}restrict` command to specify allowed roles.''',

        'success' : '''New reminder registered for <{}{}> in {} seconds. If you want to delete this reminder, type `$del`.'''
    },

    'interval' : {
        'no_argument' : '''
Usage:
    ```{prefix}interval [channel mention or user mention] <time to or time at> <interval> <message>```
Example:
    ```{prefix}interval #general 9:30 1d Good morning!```
    ```{prefix}interval 0s 10s This will be really irritating```''',

        'invalid_interval' : '''Make sure the interval you have provided is in the format of [num][s/m/h/d][num][s/m/h/d] etc. with no spaces, eg. 10s for 10 seconds or 10s12m15h1d for 10 seconds, 12 minutes, 15 hours and 1 day.''',

        '8_seconds' : '''Please make sure your interval timer is longer than 8 seconds.''',

        'donor' : '''You need to be a Patron (donating 2$ or more) to access this command! Type `{prefix}donate` to find out more.''',

        'success' : '''New interval registered for <{}{}> in {} seconds . You can\'t edit the reminder now, so you are free to delete the message.''',

        'removed' : '''There appears to be no patrons on your server, so the interval has been removed.'''

    },

    'autoclear' : {
        'disable' : '''Autoclearing disabled on {}''',

        'enable' : '''{} second autoclearing enabled.''',
    },

    'del' : {
        'listing' : '''Listing reminders on this server... (there may be a small delay, please wait for the "List (1,2,3...)" message).''',

        'listed' : '''List (1,2,3...) the reminders you wish to delete, or type anything else to cancel.''',

        'count' : '''Deleted {} reminders!'''
    },

    'todo' : {
        'server_only' : '''Please use `{prefix}todo` for your personal TODO list. `{prefix}todos` is only for server use.''',

        'add' : '''*Do `{prefix}{command} add <message>` to add an item to your TODO, or type `{prefix}{command} help` for more commands!*''',

        'too_long' : '''Sorry, but TODO message sizes are limited to 80 characters. Keep it concise :)''',

        'too_long2' : '''Sorry, but TODO lists are capped at 800 characters. Maybe, get some things done?''',

        'added' : '''Added \'{name}\' to todo!''',

        'removed' : '''Removed \'{}\' from todo!''',

        'error_value' : '''Removal item must be a number. View the numbered TODOs using `{prefix}{command}`''',

        'error_index' : '''Couldn\'t find item by that number. Are you in the correct todo list?''',

        'help' : '''To use the TODO commands, do `{prefix}{command} add <message>`, `{prefix}{command} remove <number>`, `{prefix}{command} clear` and `{prefix}{command}` to add to, remove from, clear or view your todo list.''',

        'cleared' : '''Cleared todo list!'''
    },

    'tags' : {

        'deleted' : '''Deleted tag {}''',

        'added' : '''Added tag {}''',

        'invalid_count' : '''Sorry, but for normal users tags are capped at 6 tags. Please remove some or consider donating with `{prefix}donate` ($5 tier).''',

        'invalid_chars' : '''Tags are capped at 80 characters. Keep it concise!''',

        'colon' : '''Please add a colon to split the name of the tag from the body.''',

        'illegal' : '''Please don\'t use keywords `add, new, remove, del` in the names of your tags.''',

        'unfound' : '''Couldn\'t find the tag by the name you specified.''',

        'help' : '''Use `{prefix}tag add <name>: <message>` to add new tags. Use `{prefix}tag remove <name>` to delete a tag. Use `{prefix}tag <name>` to view a tag. Use `{prefix}tag` to list all tags'''
    },

    'blacklist' : {
        'removed_from' : '''Removed blacklists from specified channels.''',

        'added_from' : '''Added specified channels to blacklist.''',

        'removed' : '''Removed current channel from blacklist.''',

        'added' : '''Added current channel to blacklist.'''

    },

    'lang' : {

        'invalid' : '''Languages:
{}''',

        'set' : '''Language set to English.''',
    },

    'clock' : {
        'time' : '''Current time is {}.''',
    }

}
