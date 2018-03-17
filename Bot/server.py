import asyncio
import zlib
import json

auths = {}

async def handle_inbound(reader, writer):
    while True:
        data = await reader.read(4096)

        try:
            data = zlib.decompress(data).decode()
        except zlib.error:
            print('Connection terminated')
            writer.close()
        else:
            if data:
                try:
                    request = json.loads(data)
                except json.decoder.JSONDecodeError:
                    print('Connection sent bad data and has been terminated')
                    writer.close()

                else:
                    connection_name = '{}:{}'.format(*writer.get_extra_info('peername'))

                    if connection_name not in auths.keys():
                        if 'token' not in request.keys():
                            writer.write()

                        self.auths[connection_name] = request['token']
            else:
                writer.close()
