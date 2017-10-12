import json

email = {}

email['email'] = input('Please enter your email: ')
email['passwd'] = input('Please enter your password: ')

with open('../email.json','w') as f:
  json.dump(email,f)
