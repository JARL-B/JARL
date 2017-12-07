import random
import discord
try:
  import wikipedia
except ImportError:
  print('Failed to locate wikipedia module.')

from globalvars import wiki_cache

async def wiki(message, client):
  m = message.content.split(' ')

  m.pop(0)

  if m:
    term = ' '.join(m)

    try:
      summary = wiki_cache[term] + ' *cached definition*'
    except KeyError:
      try:
        summary = '.'.join(wikipedia.summary(term).split('.', 2)[:2]) + '.'
      except wikipedia.exceptions.PageError:
        summary = 'Couldn\'t find page by that name.'
      except wikipedia.exceptions.DisambiguationError:
        summary = 'Disambiguation: Please try and be more specific.'

      if len(wiki_cache.keys()) > 10:
        del wiki_cache[random.choice(wiki_cache.keys())]
      wiki_cache[term] = summary

    await client.send_message(message.channel, embed=discord.Embed(title=term, description=summary))

    return

  await client.send_message(message.channel, '`$wiki`: Type the name of an item to search Wikipedia for the item.')
