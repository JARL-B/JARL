import discord
import json
from TheManagement.globalvars import tags

async def tag(message, client):
  not_done = True

  if isinstance(message.channel, discord.DMChannel):
    return

  if message.guild.id not in tags.keys():
    tags[message.guild.id] = {}

  splits = message.content.split(' ')

  if len(splits) == 1:
    if len(tags[message.guild.id]) == 0:
      await message.channel.send(embed=discord.Embed(title='No Tags!', description='*Use `$tag add <name>: <message>`, `$tag remove` and `$tag help` to manage your tags*'))
    else:
      await message.channel.send(embed=discord.Embed(title='Tags', description='\n'.join(tags[message.guild.id].keys())))

    not_done = False

  elif len(splits) > 2:
    content = ' '.join(splits[2:])

    if splits[1] in ['add', 'new']:
      if len(tags[message.guild.id]) > 5 and message.author not in get_patrons('Patrons'):
        await message.channel.send('Sorry, but for normal users tags are capped at 6. Please remove some or consider donating with `$donate` ($5 tier).')
        return

      elif len(content) > 80 and message.author not in get_patrons('Patrons'):
        await message.channel.send('Tags are capped at 80 characters. Keep it concise!')
        return

      content = content.split(':')
      if len(content) == 1:
        await message.channel.send('Please add a colon to split the name of the tag from the body.')

      else:
        if content[0].startswith(('add', 'new', 'remove', 'del')):
          await message.channel.send('Please don\'t use keywords `add, new, remove, del` in the names of your tags.')
          return

        tags[message.guild.id][content[0]] = ' '.join(content[1:]).strip()
        await message.channel.send('Added tag {}'.format(content[0]))

      not_done = False

    elif splits[1] in ['remove', 'del']:
      name = ' '.join(splits[2:])
      if name not in tags[message.guild.id].keys():
        await message.channel.send('Couldn\'t find the tag by the name you specified.')
        return

      del tags[message.guild.id][name]
      await message.channel.send('Deleted tag {}'.format(name))

      not_done = False

  if len(splits) > 1 and not_done:
    name = ' '.join(splits[1:]).strip()

    if name not in tags[message.guild.id].keys():
      await message.channel.send('Use `$tag add <name>: <message>` to add new tags. Use `$tag remove <name>` to delete a tag. Use `$tag <name>` to view a tag. Use `$tag` to list all tags')
      return

    await message.channel.send(tags[message.guild.id][name])


  with open('DATA/tags.json', 'w') as f:
    json.dump(tags, f)
