import discord
import asyncio
import sys
import os
import time
import uuid
import re
import smtplib
import random
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from globalvars import *

from RemindMe.set_reminder import set_reminder
from RemindMe.set_event import set_event
from RemindMe.set_interval import set_interval
from RemindMe.del_reminders import del_reminders

from TheManagement.autoclear import autoclear
from TheManagement.clear_channel import clear_channel
from TheManagement.spamfilter import spamfilter
from TheManagement.profanityfilter import profanityfilter
from TheManagement.serverjoin import serverjoin
from TheManagement.serverleave import serverleave
from TheManagement.verification import verification

from check_reminders import check_reminders
from change_prefix import change_prefix
from dev_tools import dev_tools
from add_blacklist import add_blacklist
from donate import donate
from update import update
from get_help import get_help


async def blacklist_msg(message):
  msg = await client.send_message(message.channel, ':x: This text channel has been blacklisted :x:')
  await client.delete_message(message)
  await asyncio.sleep(2)
  await client.delete_message(msg)


command_map = {
  'help' : get_help,
  'remind' : set_reminder,
  'event' : set_event,
  'blacklist' : add_blacklist,
  'interval' : set_interval, ## patron only ##
  'del' : del_reminders,
  'dev' : dev_tools,
  'donate' : donate,
  'update' : update,
  'clear' : clear_channel,
  'autoclear' : autoclear,
  'spam' : spamfilter,
  'profanity' : profanityfilter,
  'joinmsg' : serverjoin,
  'leavemsg' : serverleave,
  'verif' : verification
}

async def validate_cmd(message): ## method for doing the commands
  if message.server != None and message.server.id in prefix.keys():
    pref = prefix[message.server.id]
  else:
    pref = '$'

  if message.content[0] != pref: ## These functions call if the prefix isnt present
    if message.content.startswith('mbprefix'):

      if message.channel.id in channel_blacklist:
        await blacklist_msg(message)
        return

      await change_prefix(message)

    return

  cmd = message.content.split(' ')[0][1:] # extract the keyword
  if cmd in command_map.keys():

    if message.channel.id in channel_blacklist and cmd != 'help':
      await blacklist_msg(message)

      return

    else:
      await command_map[cmd](message,client)

      return

async def watch_spam(message):
  if message.author.id in users.keys(): ## all the stuff to do with smap filtering
    if time.time() - users[message.author.id] < 1:

      if message.author.id in warnings.keys():

        warnings[message.author.id] += 1
        if warnings[message.author.id] == 4:
          await client.send_message(message.channel, 'Please slow down {}'.format(message.author.mention))

        elif warnings[message.author.id] == 6:

          overwrite = discord.PermissionOverwrite()
          overwrite.send_messages = False
          await client.edit_channel_permissions(message.channel, message.author, overwrite)
          await client.send_message(message.channel, '{}, you\'ve been muted for spam. Please contact an admin to review your status.'.format(message.author.mention))

      else:
        print('user added to warning list')
        warnings[message.author.id] = 1

      users[message.author.id] = time.time()

    else:
      users[message.author.id] = time.time()
      warnings[message.author.id] = 0

  else:
    print('registered user for auto-muting')
    users[message.author.id] = time.time()

async def watch_profanity(message):
  compressed = message.content.replace(' ','').replace('-','').replace('_','')
  uid = uuid.uuid4()
  with open('profanity.exp','r') as f:
    for reg in f:
      reg = reg.strip()
      exp = re.search(reg,compressed)
      if exp: ## perform a regex search for illicit terms
        with open('DATA/profanity_issues','a') as f2:
          f2.write('{} term detected at {} (UUID {})\n'.format(exp.group(),message.author.name,uid))
        print('{} term detected at {} (UUID {})'.format(exp.group(),message.author.name,uid))
        await client.send_message(message.channel, 'Illicit term detected in input {}. If you believe this warning has been administered wrongly, please send the code `{}` to the support channel in the Discord group'.format(message.author.mention,uid))
        await client.delete_message(message)
        return


@client.event ## print some stuff to console when the bot is activated
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

    #await client.change_presence(game=discord.Game(name='$help'))


@client.event
async def on_message(message): ## when a message arrives at the bot ##
  if message.author.id == client.user.id: ## if the message has been sent by the bot ##
    return

  if message.content in ['', None]: ## if the message is a file ##
    return

  await validate_cmd(message)

  ## run stuff here if there is no command ##
  if message.channel.id in autoclears.keys(): ## autoclearing
    await asyncio.sleep(autoclears[message.channel.id])
    await client.delete_message(message)

  if message.channel.id in spam_filter:
    await watch_spam(message)

  if message.channel.id in profanity_filter:
    await watch_profanity(message)

@client.event
async def on_member_join(member):
  if member.server.id in join_messages.keys():
    await client.send_message(client.get_channel(join_messages[member.server.id][1]),join_messages[member.server.id][0].format(member.name))

  if member.server.id in verif_servers:
    while 1:
      m = await client.send_message(member, 'To verify yourself on this server, please type your email below:')
      useremail = await client.wait_for_message(channel=m.channel,author=member)

      if member.id in emails.keys() and emails[member.id] == useremail.content:
        await client.send_message(member, 'Thank you, you have already verified your email!')
        ## RUN ROLING HERE
        return

      await client.send_message(member, 'We are now sending you a verification email. Please check your inbox and if you can\'t find it, make sure to check spam folders.')

      code = ''.join([str(random.randint(0,9)) for _ in range(8)]) # generate an 8 digit verification code

      server = smtplib.SMTP('smtp.gmail.com',587)

      server.ehlo()
      server.starttls()

      with open('email.json','r') as f:
        email = json.load(f)

      server.login(email['email'], email['passwd'])

      text = '''
  <h1>Hello, {name}</h1>
  Please use the verification code below to verify your Discord user on {server}:
  <br>
  <strong>{code}</strong>
  <br>
  Simply DM the code to the BOT and you'll be immediately verified! Thank you for using TheManagement.
  '''.format(name=member.name,server=member.server.name,code=code)

      msg = MIMEMultipart()
      msg['From'] = email['email']
      msg['To'] = useremail.content
      msg['Subject'] = 'Verify Your Presence on {}'.format(member.server.name)

      msg.attach(MIMEText(text, 'html'))

      try:
        server.sendmail(email['email'], [useremail.content], msg.as_string())
      except:
        await client.send_message(m.channel, 'Oh no :( There was an error sending the verification email. Please try again later')

      server.close()

      code_in = await client.wait_for_message(channel=m.channel,author=member)

      if code_in.content == code:
        await client.send_message(m.channel, 'Thank you for verifying your account!')
        emails[member.id] = useremail.content

        with open('DATA/emails.json','w') as f:
          json.dump(emails,f)

        ## RUN ROLING HERE

        return
      else:
        await client.send_message(m.channel, 'Incorrect code entered. Please try again...')


@client.event
async def on_member_remove(member):
  if member.server.id in leave_messages.keys():
    await client.send_message(client.get_channel(leave_messages[member.server.id][1]),leave_messages[member.server.id][0].format(member.name))

try: ## token grabbing code
  with open('token','r') as token_f:
    token = token_f.read().strip('\n')

except FileNotFoundError:
  if len(sys.argv) < 2:
    print('Please remember you need to enter a token for the bot as an argument, or create a file called \'token\' and enter your token into it.')
  else:
    token = sys.argv[1]

else:
  try:
    client.loop.create_task(check_reminders())
    client.run(token)
  except:
    print('Error detected. Restarting in 15 seconds.')
    time.sleep(15)

    os.execl(sys.executable, sys.executable, *sys.argv)
