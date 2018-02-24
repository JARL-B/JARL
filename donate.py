from globalvars import *

async def donate(message, client):
    await message.channel.send(
    '''
    Thinking of adding a monthly contribution? Press below for my patreon and official bot server :D
    https://www.patreon.com/jellywx

    https://discord.gg/WQVaYmT

    Here's some more information:

    When you donate, Patreon will automatically rank you up on our Discord server, supposing you have properly linked your Patreon and Discord accounts!
    With your new rank, you'll be able to:
    : chat on the Patron-only chat
    : use Patron-only commands like `interval`
    : set more reminders
    : set longer reminders
    : set more/longer tags
    : use the Patron-only `TrackerBot` to track your game time through Discord

    Anyone who is a Patron, thank you :D You make this bot sustainable

    Please note, you must be connected to the Discord server to receive Patreon rewards.
    '''
    )
