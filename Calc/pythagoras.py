async def pythagoras(message,client):
  text = message.content.split(' ',1)[1].lower()
  params = text.split(' ')
  variables = {
    'a' : None,
    'b' : None,
    'c' : None
  }

  provided = 0

  try:
    for p in params:
      if p[0] == 'a' and not variables['a']:
        variables['a'] = float(p.split('=')[1])
        provided += 1
      elif p[0] == 'b' and not variables['b']:
        variables['b'] = float(p.split('=')[1])
        provided += 1
      elif p[0] == 'c' and not variables['c']:
        variables['c'] = float(p.split('=')[1])
        provided += 1
      else:
        await client.send_message(message.channel, 'No option for variable {}. Please enter data like so: `$pythagoras a=NUM b=NUM c=NUM`, with 2 of `a`, `b` or `c` entered'.format(p[0]))
        return
  except ValueError:
    await client.send_message(message.channel, 'Failed to change one of your variables to a number. Please make sure that you have correctly entered the values `a`, `b` and/or `c`')
    return

  if provided > 2:
    await client.send_message(message.channel, 'You entered all the values... what do you need me for?')
    return

  elif provided < 2:
    await client.send_message(message.channel, 'I need at least 2 values to calculate. Please enter data like so: `$pythagoras a=NUM b=NUM c=NUM`, with 2 of `a`, `b` or `c` entered')
    return

  if variables['a']:
    if variables['b']:
      missing = (variables['a']**2 + variables['b']**2)**0.5

    else:
      if variables['c'] < variables['a']:
        await client.send_message(message.channel, 'Side length `c` (hypo) cannot be greater than side length `a` or `b` (width|height)')
        return
      missing = (variables['c']**2 - variables['a']**2)**0.5

  else:
    if variables['c'] < variables['b']:
      await client.send_message(message.channel, 'Side length `c` (hypo) cannot be greater than side length `a` or `b` (width|height)')
      return
    missing = (variables['c']**2 - variables['b']**2)**0.5

  await client.send_message(message.channel, 'Missing length is {}, to 4 d.p (please note that if you want the result to be more accurate, you need to use a proper calculator)'.format(round(missing,4)))
