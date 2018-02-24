class Reminder():
  def __init__(self, *, dictv=None, interval=None, time=0, message="", channel=None):
    if dictv != None:
      self.interval = dictv['interval']
      self.time = int(dictv['time'])
      self.message = str(dictv['message'])
      self.channel = int(dictv['channel'])

    else:
      self.interval = interval
      self.time = int(time)
      self.message = str(message)
      self.channel = int(channel)

  def __lt__(self, comparison):
    return self.time < comparison.time

  '''def __dict__(self):
    return {
      'time' : self.time,
      'interval' : self.interval,
      'message' : self.message,
      'channel' : self.channel
    }'''
