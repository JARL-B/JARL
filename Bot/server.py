import asyncio
import zlib
import json

from globalvars import client, cursor

auths = {}
users = {}

def pack_data(data: dict):
    return zlib.compress(json.dumps(data).encode())

def close(n):
    try:
        del auths[n]
        del users[n]
    except KeyError:
        pass

async def handle_inbound(reader, writer):
    while True:
        connection_name = '{}:{}'.format(*writer.get_extra_info('peername'))

        data = await reader.read(4096)

        try:
            data = zlib.decompress(data).decode()
        except zlib.error:
            print('Connection terminated')
            writer.close()
            close(connection_name)
            return
        else:
            if data:
                try:
                    request = json.loads(data)
                except json.decoder.JSONDecodeError:
                    print('Connection sent bad data and has been terminated')
                    writer.write(pack_data({'err' : 'JASON ONLY'}))
                    writer.close()
                    close(connection_name)
                    return

                else:
                    if connection_name not in auths.keys():
                        if 'token' not in request.keys():
                            writer.write(pack_data({'err' : 'UNAUTHORIZED'}))
                            writer.close()
                            close(connection_name)
                            return
                        else:
                            values = dict(cursor.execute('''SELECT * FROM users WHERE token = ?''', (request['token'],)))
                            if values:
                                auths[connection_name] = request['token']
                                users[connection_name] = list(values.keys())[0]
                                writer.write(pack_data({'user' : list(values.keys())[0]}))
                            else:
                                writer.write(pack_data({'err' : 'UNAUTHORIZED'}))
                                writer.close()
                                close(connection_name)
                                return

                    else:
                        values = dict(cursor.execute('''SELECT * FROM users WHERE token = ?''', (auths[connection_name],)))
                        if not values:
                            writer.write(pack_data({'err' : 'AUTHORIZATION CHANGED'}))
                            writer.close()
                            close(connection_name)
                            return

                        if 'do' not in request.keys():
                            writer.write(pack_data({'err' : 'BAD PACKAGE'}))
                            writer.close()
                            close(connection_name)
                            return

                        if request['do'] == 'grab_servers':
                            shared_servers = [guild for guild in client.guilds if guild.get_member(users[connection_name]) is not None and guild.get_member(users[connection_name]).guild_permissions.manage_messages]

                            writer.write(pack_data({'servers' : [[s.name, s.id] for s in shared_servers]}))

                        elif request['do'] == 'put':
                            pass

            else:
                writer.close()
                return
