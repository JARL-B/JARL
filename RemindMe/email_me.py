import json

from RemindMe.globalvars import mail_list

from TheManagement.globalvars import emails

from register_email import register_email
from get_patrons import get_patrons

async def email_me(message,client):
  if message.author in get_patrons(level='Donor'):
    if message.author.id in emails.keys():
      if message.channel.id not in mail_list.keys():
        mail_list[message.channel.id] = []

      if message.author.id in mail_list[message.channel.id]:
        mail_list[message.channel.id].remove(message.author.id)
        await client.send_message(message.channel, 'Disabled email reminders!')

      else:
        mail_list[message.channel.id].append(message.author.id)
        await client.send_message(message.channel, 'All reminders (not intervals) in this channel will now be emailed to you!')

      with open('DATA/mail_list.json','w') as f:
        json.dump(mail_list,f)

    else:
      await client.send_message(message.channel, 'First you must verify your email! Check your DMs!')
      await register_email(message.author)

  else:
    await client.send_message(message.channel, 'You must be a donor (donating 2$ or more) to use this command! Type `$donate` for more information.')
