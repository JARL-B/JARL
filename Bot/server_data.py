import json

class ServerData(object):
    def __init__(self, **entries):
        self.__dict__.update(entries)

        self.blacklist = json.loads(self.blacklist)
        self.restrictions = json.loads(self.restrictions)
        self.tags = json.loads(self.tags)
        self.autoclears = json.loads(self.autoclears)

    def __repr__(self):
        return 'ServerData:' + str(self.__dict__)
