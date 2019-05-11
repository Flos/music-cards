from mpd import MPDClient
from Reader import Reader

import re
import sys
import time


def connectMPD():
	try:
		client = MPDClient()               # create client object
		client.timeout = 200               # network timeout in seconds (floats allowed), default: None
		client.idletimeout = None
		client.connect("localhost", 6600)
		return client
	except:
		print 'Could not connect to MPD server'

def clear_and_play(client, plist):
	try:
		client.stop()
		client.clear()
		if re.compile("mopidy:").match(plist): #local mopidy playlist 
			plist=plist.replace("mopidy:", "")
			client.clear()
			client.load(plist)
			client.random(1)
		else: #file or spotify url
			client.add(plist)
			client.repeat(1)
		client.play()
	except:
		print 'Could not play playlist %s' % plist


reader = Reader()
client = None
before_card = None
before_volume = None
while not client:
	client = connectMPD()
	if not client:
		time.sleep(2)

print 'Ready: place a card on top of the reader'

while True:
	try:
		card = reader.readCard()
		print "Read card!"
		client = connectMPD()
		if card != '' and card != before_volume and re.compile("volume:").match(card): #volume card -> set new volume
			print "Volume card found."
			before_volume = card
			card=card.replace("volume:", "")
			client.setvol(card)
		elif card != '' and card != before_card and not re.compile("volume:").match(card): #if card isn't empty and card isn't the same before
			print "Music card found."
			clear_and_play(client, card)
			before_card = card
		elif card == before_card and not re.compile("volume:").match(card): #same card like before
			print "Same card."
			if client.status()["state"] != "play":
				client.play()
		client.close()
		
		reader.released_Card()
		
		client = connectMPD()
		if client.status()["state"] != "pause":
			client.pause()
		client.close()

	except KeyboardInterrupt:
		sys.exit(0)

	except ValueError:
		print "this card is new"
		print "need to Set a playlist"
		reader.released_Card()

	except:
		pass
