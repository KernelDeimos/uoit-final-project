from chromeCastControl import Chromecasts
from smartSwitchControl import Plugs

theCasts = Chromecasts()
thePlugs = Plugs()
castsResult = theCasts.findCasts()
plugsResult = thePlugs.findPlugs()
print(castsResult)
print(" ")
print(plugsResult)


