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
        page = wikipedia.page(term)
        summary = wikipedia.summary(term, sentences=2)
        try:
          img = [i for i in page.images if i.lower().endswith('jpg') or i.lower().endswith('png') or i.lower().endswith('bmp') or i.lower().endswith('jpeg')][0]
        except IndexError:
          img = ''
      except wikipedia.exceptions.PageError:
        summary = 'Couldn\'t find page by that name.'
      except wikipedia.exceptions.DisambiguationError:
        summary = 'Disambiguation: Please try and be more specific.'

      if len(wiki_cache.keys()) > 10:
        del wiki_cache[random.choice(wiki_cache.keys())]
      wiki_cache[term] = summary

    em = discord.Embed(title=page.title, description=summary)
    try:
      em.set_image(url=img)
    except:
      pass

    await client.send_message(message.channel, embed=em)

    return

  await client.send_message(message.channel, '`$wiki`: Type the name of an item to search Wikipedia for the item.')
