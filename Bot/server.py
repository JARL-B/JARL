import asyncio
import zlib
import json

async def handle_inbound(reader, writer):
    data = await reader.read(4096)
    data = zlib.decompress(data).decode()
    print('Received {} from {}'.format(data, writer.get_extra_info('peername')))

#loop = asyncio.get_event_loop()
#coro = asyncio.start_server(handle_inbound, 'localhost', 44139, loop=loop)
#server = loop.run_until_complete(coro)

#try:
#    loop.run_forever()
#except KeyboardInterrupt:
#    pass

#server.close()
#loop.run_until_complete(server.wait_closed())
#loop.close()
