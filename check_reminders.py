import discord
import asyncio
from globalvars import *
import time
import csv
import json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from itertools import chain


async def check_reminders():
  await client.wait_until_ready()
  while not client.is_closed:
    for reminder in calendar:
      if int(reminder[0]) <= time.time():
        users = client.get_all_members()
        channels = client.get_all_channels()

        msg_points = chain(users, channels)

        recipient = discord.utils.get(msg_points,id=reminder[1])

        try:
          await client.send_message(recipient,reminder[2])
          print('Administered reminder to ' + recipient.name)

          if recipient.id in mail_list.keys():
            text = '''
              <h1>Reminder from {recipient.server.name}</h1>
              {reminder[2]}<br>
              <em>Thank you for using TheManagement.</em>
              '''.format(recipient=recipient,reminder=reminder)

            msg = MIMEMultipart()
            msg['From'] = mailserver.email['email']
            msg['Subject'] = 'Reminder on {}'.format(recipient.name)

            mailserver.open()

            for uid in mail_list[recipient.id]:

              msg['To'] = emails[uid]

              msg.attach(MIMEText(text, 'html'))
              mailserver.mail.sendmail(mailserver.email['email'], [msg['To']], msg.as_string())

            mailserver.close()

        except:
          print('Couldn\'t find required channel. Skipping a reminder')

        calendar.remove(reminder)

    for inv in intervals:
      if int(inv[0]) <= time.time():
        channels = client.get_all_channels()

        recipient = discord.utils.get(channels,id=inv[2])

        try:
          await client.send_message(recipient,inv[3])
          print('Administered interval to ' + recipient.name)

          print(inv)
          inv[0] = str(int(inv[0]) + int(inv[1])) ## change the time for the next interval
        except:
          print('Couldn\'t find required channel. Skipping an interval')
          intervals.remove(inv)


    with open('DATA/calendar.csv','w') as f:
      writer = csv.writer(f,delimiter=',',lineterminator=';')
      writer.writerows(calendar) ## uses a CSV writer to write the data to file.

    with open('DATA/intervals.csv','w') as f:
      writer = csv.writer(f,delimiter=',',lineterminator=';')
      writer.writerows(intervals) ## uses a CSV writer to write the data to file.

    await asyncio.sleep(1.5)
