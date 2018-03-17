import asyncio
import zlib
import json

from globalvars import client, cursor

auths = {}

async def handle_inbound(reader, writer):
    while True:
        data = await reader.read(4096)

        try:
            data = zlib.decompress(data).decode()
        except zlib.error:
            print('Connection terminated')
            writer.close()
            return
        else:
            if data:
                try:
                    request = json.loads(data)
                except json.decoder.JSONDecodeError:
                    print('Connection sent bad data and has been terminated')
                    writer.close()
                    return

                else:
                    connection_name = '{}:{}'.format(*writer.get_extra_info('peername'))

                    if connection_name not in auths.keys():
                        if 'token' not in request.keys():
                            writer.write(zlib.compress(json.dumps({'err' : 'UNAUTHORIZED'}).encode()))
                            writer.close()
                            return
                        else:
                            values = dict(cursor.execute('''SELECT * FROM users WHERE token = ?''', (request['token'],)))
                            if values:
                                auths[connection_name] = request['token']
                                writer.write(zlib.compress(json.dumps({'user' : list(values.keys())[0]}).encode()))
                            else:
                                writer.write(zlib.compress(json.dumps({'err' : 'UNAUTHORIZED'}).encode()))
                                writer.close()
                                return
            else:
                writer.close()
