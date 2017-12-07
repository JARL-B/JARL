import discord
try:
  import wikipedia
except ImportError:
  print('Failed to locate wikipedia module.')

async def wiki(message, client):
  m = message.content.split(' ')

  m.pop(0)

  if m:
    term = ' '.join(m)

    try:
      summary = '.'.join(wikipedia.summary(term).split('.', 2)[:2]) + '.'
    except wikipedia.exceptions.PageError:
      summary = 'Couldn\'t find page by that name.'
    except wikipedia.exceptions.DisambiguationError:
      summary = 'Disambiguation: Please try and be more specific.'

    await client.send_message(message.channel, embed=discord.Embed(title=term, description=summary))

    return

  await client.send_message(message.channel, '`$wiki`: Type the name of an item to search Wikipedia for the item.')
