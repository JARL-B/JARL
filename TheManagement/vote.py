import asyncio

from globalvars import votes

async def vote(message,client):
  if len(message.content.split(' ')) == 1:
    await client.send_message(message.channel,'You need to provide some text for your vote!')
  else:
    msg = await client.send_message(message.channel,message.content.split(' ',1)[1])

    await client.add_reaction(msg,'❎')
    await client.add_reaction(msg,'✅')

    v = Vote(msg)

    votes.append(v)

    await asyncio.sleep(600)

    positive = v.pos_v
    negative = v.neg_v

    total = positive + negative
    p_perc = positive / total
    n_perc = negative / total

    await client.send_message(message.channel, 'Vote results are in!\n Total votes: {t},\n Positive votes: {p},\n Negative votes: {n},\n Percents: {r} in favor to {rn} in contest'.format(t=total,p=positive,n=negative,r=p_perc,rn=n_perc))

class Vote(object):
  def __init__(self,message):
    self.message = message
    self.pos_v = 0
    self.neg_v = 0
