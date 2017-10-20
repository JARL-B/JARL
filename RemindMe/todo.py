import json
from discord import Embed

from globalvars import todos

async def todo(message,client):
  if message.author.id not in todos.keys():
    todos[message.author.id] = []

  splits = message.content.split(' ')

  todo = todos[message.author.id]

  if len(splits) == 1:
    msg = ['\n{}: {}'.format(i+1,todo[i]) for i in range(len(todo))]
    if len(msg) == 0:
      msg.append('*Do `$todo add <message>` to add an item to your TODO, or type `$todo help` for more commands!*')
    await client.send_message(message.channel, embed=Embed(title='{}\'s TODO'.format(message.author.name), description=''.join(msg)))

  elif len(splits) > 2:
    if splits[1] in ['add','append','push']:
      a = ' '.join(splits[2:])
      todos[message.author.id].append(a)
      await client.send_message(message.channel, 'Added \'{}\' to todo!'.format(a))

    elif splits[1] in ['remove','r','del','rm']:
      try:
        a = todos[message.author.id].pop(int(splits[2])-1)
        await client.send_message(message.channel, 'Removed \'{}\' from todo!'.format(a))

      except ValueError:
        await client.send_message(message.channel, 'Removal item must be a number. View the numbered TODOs using `$todo`')

    else:
      await client.send_message(message.channel, 'To use the TODO commands, do `$todo add <message>`, `$todo remove <number>`, `$todo clear` and `$todo` to add to, remove from, clear or view your todo list.')

  elif splits[1] in ['remove*','r*','del*','rm*', 'clear', 'clr']:
    todos[message.author.id] = []
    await client.send_message(message.channel, 'Cleared todo list!')

  else:
    await client.send_message(message.channel, 'To use the TODO commands, do `$todo add <message>`, `$todo remove <number>`, `$todo clear` and `$todo` to add to, remove from, clear or view your todo list.')

  with open('DATA/todos.json','w') as f:
    json.dump(todos,f)
