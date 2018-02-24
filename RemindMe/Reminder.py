class Reminder():
    def __init__(self, *, dictv=None, interval=None, time=0, message="", channel=None):
        if dictv != None:
            if dictv['interval'] == None:
                self.interval = dictv['interval']
            else:
                self.interval = int(dictv['interval'])
            self.time = int(dictv['time'])
            self.message = str(dictv['message'])
            self.channel = int(dictv['channel'])

        else:
            if interval == None:
                self.interval = interval
            else:
                self.interval = int(interval)
            self.time = int(time)
            self.message = str(message)
            self.channel = int(channel)

    def __lt__(self, comparison):
        return self.time < comparison.time
