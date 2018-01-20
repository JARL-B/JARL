import json
from discord import Embed

from globalvars import todos

async def server_todo(message, client):
  if message.guild.id not in todos.keys():
    todos[message.guild.id] = []

  splits = message.content.split(' ')

  todo = todos[message.guild.id]

  if len(splits) == 1:
    msg = ['\n{}: {}'.format(i+1,todo[i]) for i in range(len(todo))]
    if len(msg) == 0:
      msg.append('*Do `$todo add <message>` to add an item to your TODO, or type `$todo help` for more commands!*')
    await message.channel.send(embed=Embed(title='{}\'s TODO'.format(message.guild.name), description=''.join(msg)))

  elif len(splits) > 2:
    if splits[1] in ['add','a','append','push']:
      a = ' '.join(splits[2:])
      if len(a) > 40:
        await message.channel.send('Sorry, but TODO message sizes are limited to 40 characters. Keep it concise :)')
        return

      elif len(''.join(todo)) > 400:
        await message.channel.send('Sorry, but TODO lists are capped at 400 characters. Maybe, get some things done?')
        return

      todos[message.guild.id].append(a)
      await message.channel.send('Added \'{}\' to todo!'.format(a))

    elif splits[1] in ['remove','r','del','rm']:
      try:
        a = todos[message.guild.id].pop(int(splits[2])-1)
        await message.channel.send('Removed \'{}\' from todo!'.format(a))

      except ValueError:
        await message.channel.send('Removal item must be a number. View the numbered TODOs using `$todo`')

    else:
      await message.channel.send('To use the TODO commands, do `$todo add <message>`, `$todo remove <number>`, `$todo clear` and `$todo` to add to, remove from, clear or view your todo list.')

  elif splits[1] in ['remove*','r*','del*','rm*', 'clear', 'clr']:
    todos[message.guild.id] = []
    await message.channel.send('Cleared todo list!')

  else:
    await message.channel.send('To use the TODO commands, do `$todo add <message>`, `$todo remove <number>`, `$todo clear` and `$todo` to add to, remove from, clear or view your todo list.')

  with open('DATA/todos.json','w') as f:
    json.dump(todos, f)
