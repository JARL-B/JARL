import json
import smtplib
import random
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from globalvars import client, emails

async def register_email(member):
  while 1:
    m = await client.send_message(member, 'To verify yourself on this server, please type your email below:')
    useremail = await client.wait_for_message(channel=m.channel,author=member)

    if member.id in emails.keys() and emails[member.id] == useremail.content:
      await client.send_message(member, 'Thank you, you have already verified your email!')

      try:
        await client.add_roles(member, discord.utils.get(member.server.roles, name='Manager:Email Verified'))
      except:
        pass

      return

    await client.send_message(member, 'We are now sending you a verification email. Please check your inbox and if you can\'t find it, make sure to check spam folders. When you receive the email, send the code below:')

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

      try:
        await client.add_roles(member, discord.utils.get(member.server.roles, name='Manager:Email Verified'))
      except:
        pass

      return
    else:
      await client.send_message(m.channel, 'Incorrect code entered. Please try again...')
