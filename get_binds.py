from globalvars import *

def get_binds():
  return [bind for user in binds.values() for bind in user] 
