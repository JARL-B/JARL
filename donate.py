from globalvars import *

async def donate(message,client):
  await client.send_message(message.channel,
  '''
  Thinking of donating? Press below for my patreon and official bot server :D
  https://www.patreon.com/jellywx

  https://discord.gg/WQVaYmT

  Here's some more information:

  When you donate, Patreon will automatically rank you up on our Discord server, supposing you have properly linked your Patreon and Discord accounts!
  With your new rank, you'll be able to:
  : chat on the Patron-only chat (which is more frequented by myself)
  : pass your suggestions straight to me, rather than sending them to a file on my server
  : use Patron-only commands like ~`bind`~ (still WIP) and `interval`
  : let me make a cup of coffee once a month

  Anyone who is a Patron, thank you :D You make this bot sustainable
  '''
  )
