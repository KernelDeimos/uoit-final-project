from pyHS100 import (Discover, SmartPlug)
from pprint import pprint
import json, time

plugs = []

class Plugs():

	def findPlugs(self):
		global plugs
		plugs = []
		for item in Discover.discover():
			#Refresh plug list every time search is run
			plug = SmartPlug(item)
			plugInfo = (plug.get_sysinfo())
			name = plugInfo['alias']
			hostIP = item
			plugs.append([name, hostIP])

	def turnOn(self, name):
		global plugs
		for item in plugs:
			if item[0] == name:
				chosen = SmartPlug(item[1])
				chosen.state = "ON"
				break

	def turnOff(self, name):
		global plugs
		for item in plugs:
			if item[0] == name:
				chosen = SmartPlug(item[1])
				chosen.state = "OFF"
				break

test = Plugs()
test.findPlugs()

test.turnOn("Living Room Receiver")
#time.sleep(2)
#test.turnOff("Bedroom Audio")
