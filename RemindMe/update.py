import asyncio
import subprocess
import os
import sys

from globalvars import *
from get_patrons import get_patrons

async def update(message):
  if message.author in get_patrons('Staff'):
    await client.change_presence(game=discord.Game(name='updating... hold on tight!'))

    print('Running pull...')
    subprocess.call(['git', 'pull'])

    print('Restarting now!')
    os.execl(sys.executable, sys.executable, *sys.argv)
