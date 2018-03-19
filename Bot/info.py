import discord

from globalvars import prefix
from sloccount import sloccount_py

async def info(message, client):
    if message.guild != None and message.guild.id in prefix.keys():
        pref = prefix[message.guild.id]
    else:
        pref = '$'

    em = discord.Embed(title='**INFO**',description=
    '''\u200B
    Default prefix: `$`
    Reset prefix: `mbprefix $`
    Help: `{p}help`

    **Welcome to RemindMe!**
    Developer: <@203532103185465344>
    Cool guy who knows what he's on about: <@174243954487853056>
    Icon: <@253202252821430272>
    Find me on https://discord.gg/WQVaYmT and on https://github.com/JellyWX :)

    Framework: `discord.py`
    Total SᵒᵘʳᶜᵉLᶦⁿᵉˢOᶠCᵒᵈᵉ: {sloc} (100% Python)
    Hosting provider: OVH

    My other bot (Patron only):
    https://discordapp.com/oauth2/authorize?client_id=411224415863570434&scope=bot&permissions=35840

    *If you have enquiries about new features, please send to the discord server*
    *If you have enquiries about bot development for you or your server, please DM me*
    '''.format(p=pref, sloc=sloccount_py('.'))
    )

    await message.channel.send(embed=em)

    await message.add_reaction('📬')
