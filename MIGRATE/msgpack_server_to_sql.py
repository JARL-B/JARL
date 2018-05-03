import msgpack
import zlib
import sqlite3
import json


with open('../DATA/data.msgpack.zlib', 'rb') as f:
    data = msgpack.unpackb(zlib.decompress(f.read()), encoding='utf8')

with sqlite3.connect('../DATA/calendar.db') as connection:
    cursor = connection.cursor()
    for clump in data:
        print(clump)

        command = '''INSERT INTO servers (id, prefix, timezone, language, blacklist, restrictions, tags, autoclears)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)'''

        cursor.execute(command, (clump['id'], clump['prefix'], clump['timezone'], clump['language'], json.dumps(clump['blacklist']), json.dumps(clump['restrictions']), json.dumps(clump['tags']), json.dumps(clump['autoclears'])))
