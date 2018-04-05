import json
import discord
from discord import Embed

from globalvars import todos

async def todo(message,client):
    if 'todos' in message.content.split(' ')[0]:
        if isinstance(message.channel, discord.DMChannel):
            await message.channel.send('Please use `$todo` for your personal TODO list. `$todos` is only for server use.')
            return

        location = message.guild.id
        name = message.guild.name
        command = 'todos'
    else:
        location = message.author.id
        name = message.author.name
        command = 'todo'


    if location not in todos.keys():
        todos[location] = []

    splits = message.content.split(' ')

    todo = todos[location]

    if len(splits) == 1:
        msg = ['\n{}: {}'.format(i+1,todo[i]) for i in range(len(todo))]
        if len(msg) == 0:
            msg.append('*Do `${0} add <message>` to add an item to your TODO, or type `${0} help` for more commands!*'.format(command))
        await message.channel.send(embed=Embed(title='{}\'s TODO'.format(name), description=''.join(msg)))

    elif len(splits) > 2:
        if splits[1] in ['add', 'a']:
            a = ' '.join(splits[2:])
            if len(a) > 80:
                await message.channel.send('Sorry, but TODO message sizes are limited to 80 characters. Keep it concise :)')
                return

            elif len(''.join(todo)) > 800:
                await message.channel.send('Sorry, but TODO lists are capped at 800 characters. Maybe, get some things done?')
                return

            todos[location].append(a)
            await message.channel.send('Added \'{}\' to todo!'.format(a))

        elif splits[1] in ['remove', 'r']:
            try:
                a = todos[location].pop(int(splits[2])-1)
                await message.channel.send('Removed \'{}\' from todo!'.format(a))

            except ValueError:
                await message.channel.send('Removal item must be a number. View the numbered TODOs using `${}`'.format(command))
            except IndexError:
                await message.channel.send('Couldn\'t find item by that number. Are you in the correct todo list?')

        else:
            await message.channel.send('To use the TODO commands, do `${0} add <message>`, `${0} remove <number>`, `${0} clear` and `${0}` to add to, remove from, clear or view your todo list.'.format(command))

    elif splits[1] in ['remove*', 'r*', 'clear', 'clr']:
        todos[location] = []
        await message.channel.send('Cleared todo list!')

    else:
        await message.channel.send('To use the TODO commands, do `${0} add <message>`, `${0} remove <number>`, `${0} clear` and `${0}` to add to, remove from, clear or view your todo list.'.format(command))

    with open('DATA/todos.json','w') as f:
        json.dump(todos,f)
