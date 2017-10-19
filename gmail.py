import json
import smtplib

class gmail(object):
  def __init__(self):
    self.mail = None

    with open('email.json','r') as f:
      self.email = json.load(f)

  def open(self):
    self.mail = smtplib.SMTP('smtp.gmail.com',587)

    self.mail.ehlo()
    self.mail.starttls()

    self.mail.login(self.email['email'], self.email['passwd'])

  def close(self):
    self.mail.close()
