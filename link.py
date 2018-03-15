import sqlite3
import discord
import uuid

from globalvars import cursor, connection

async def link(message, client):
    if not isinstance(message.channel, discord.DMChannel):
        await message.channel.send('Please execute this command in a DM')

    command = '''SELECT * FROM users WHERE id = ?'''

    token = uuid.uuid1()
    entry = cursor.execute(command, (message.author.id,))
    if dict(entry):
        command = '''DELETE FROM users WHERE id = ?'''
        cursor.execute(command, (message.author.id,))

    command = '''INSERT INTO users (id, token)
    VALUES (?, ?)'''

    cursor.execute(command, (message.author.id, token.hex.replace('-', '')))
    connection.commit()

    await message.channel.send('Your new access token is `{}`. Use `$link` to reset it if necessary.'.format(token))
