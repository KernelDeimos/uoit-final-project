import pychromecast, sys, time, subprocess
from spotifyControl import *
from smartSwitchControl import *
from gtts import gTTS

chromecasts = None
availableCasts = []
chromecasts = []
wanted = None

class Chromecasts():

	def findCasts(self):
		global chromecasts
		chromecasts = pychromecast.get_chromecasts()
		for item in chromecasts:
			chromecast = item.device.friendly_name
			id = str(item.device.uuid)
			id.replace('UUID(', '')
			id.replace(')', '')
			availableCasts.append([chromecast, id])
		return availableCasts

	def cast(self):
		cast = None
		global availableCasts
		plugs = Plugs()
		for devices in availableCasts:
			for obj in chromecasts:
				#Comission Google Home Device for local control of chromecasts
				if obj.device.friendly_name == "Home":
					commandNode = pychromecast.Chromecast("192.168.1.20")
					commandNode.wait()
				if obj.device.friendly_name == "Whole Home Audio":
					plugs.turnOn("Living Room Receiver")
					print("Living Room Receiver: On")
					plugs.turnOn("Bedroom Receiver")
					print("Bedroom Receiver: On")
					plugs.turnOn("Basement Receiver")
					print("Basement Receiver: On")
					castNode = next(cc for cc in chromecasts if cc.device.friendly_name == "Whole Home Audio")
					castNode.wait()
					activate = castNode.media_controller
					ID = str(castNode.device.uuid)
					tunes = Music()
					tunes.chooseMusic(ID)
					print("Playing Music on Chromecast: ", obj.device.friendly_name)
					break
			break

	def pause(self):
		self.pause()

system = Chromecasts()
system.findCasts()

system.cast()

