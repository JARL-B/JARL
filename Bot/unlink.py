from globalvars import cursor

async def unlink(message, client):
    cursor.execute('DELETE FROM users WHERE id = ?', (message.author.id,))
    await message.channel.send('You have been unlinked. Use `$link` to generate a token.')
