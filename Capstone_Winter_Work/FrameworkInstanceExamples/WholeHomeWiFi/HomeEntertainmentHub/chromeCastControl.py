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
			id = item.device.uuid
			availableCasts.append([chromecast, id])

	def cast(self):
		cast = None
		global availableCasts
		print("DEVICES: ", availableCasts)
		switches = Plugs()
		switches.findPlugs()
		for devices in availableCasts:
			for obj in chromecasts:
				print("OBSERVED OBJECT: ", obj.device.friendly_name)
				if obj.device.friendly_name == "Home":
					#EFFORTS TO BACK DOOR FORCE CONTROL OF CHROMECAST ACTIVATIONS THROUGH GOOGLE HOME VOICE COMMAND
					#tts = gTTS("Play rock on Whole Home Audio", lang='en')
					commandNode = pychromecast.Chromecast("192.168.1.20")
					commandNode.wait()
					#gHome = commandNode.media_controller
					#gHome.play_media(json.loads(tts), "audio/mp3")
					print("found home")
				if obj.device.friendly_name == "Whole Home Audio":
					switches.turnOn("Living Room Receiver")
					switches.turnOn("Bedroom Receiver")
					switches.turnOn("Basement Receiver")
					castNode = next(cc for cc in chromecasts if cc.device.friendly_name == "Whole Home Audio")
					castNode.wait()
					activate = castNode.media_controller
					#USED FOR HARD FILE REFERENCE
					#activate.play_media("http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4", "video/mp4")
					#GOOGLE ADDS AND REMOVES - FOR IDs. CREATE SEARCH METHOD TO INHERENTLY KNOW WHEN THERE OR NOT AND REMOVE IF NOT
					#ID = str(castNode.device.uuid).replace("-","")
					ID = str(castNode.device.uuid)
					tunes = Music()
					tunes.chooseMusic(ID)
					print("ID ", ID)
					#ALLOWS FOR INTERNAL CALL TO SPOTIFYCONTROL.PY. MIGHT NOT NEED
					#subprocess.call(playThis)
					break
			break

	def pause(self):
		self.pause()

test = Chromecasts()
test.findCasts()
test.cast()

