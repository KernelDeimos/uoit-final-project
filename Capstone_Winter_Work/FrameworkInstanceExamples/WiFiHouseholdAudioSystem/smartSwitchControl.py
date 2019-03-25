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
			if plugInfo['relay_state'] == 0:
				status = "OFF"
			elif plugInfo['relay_state'] == 1:
				status = "ON"
			hostIP = item
			UUID = plugInfo['deviceId']
			plugs.append([name, hostIP, status, UUID])
		return plugs

	def turnOn(self, UUID):
		global plugs
		self.findPlugs()
		for item in plugs:
			if item[3] == UUID:
				chosen = SmartPlug(item[1])
				chosen.state = "ON"
				break

	def turnOff(self, UUID):
		global plugs
		self.findPlugs()
		for item in plugs:
			if item[3] == UUID:
				chosen = SmartPlug(item[1])
				chosen.state = "OFF"
				break

#switchControl = Plugs()
#switchControl.findPlugs()

#print(plugs)

