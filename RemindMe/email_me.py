from RemindMe.globalvars import mail_list

from TheManagement.globalvars import emails

from register_email import register_email

async def email_me(message,client):
  if message.author in get_patrons(level='Donor'):
    if message.author.id in emails.keys():
      if message.channel.id not in mail_list.keys():
        mail_list[message.channel.id] = []
      await client.send_messages(message.channel, 'All reminders in this channel will now be emailed to you!')

    else:
      await client.send_message(message.channel, 'First you must verify your email!')
      await register_email(message.author)

  else:
    await client.send_message(message.channel, 'You must be a donor (donating 2$ or more) to use this command! Type `$donate` for more information.')
