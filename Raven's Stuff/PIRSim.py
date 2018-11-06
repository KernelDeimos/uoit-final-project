import occupantSim
import json
import time

sensorName = "PIR Sensor"
occupants = 0

while True:
    occupancy = {'sensorData': {'SensorID': sensorName, 'Occupants': occupants}}
    occupants = occupantSim.occupancyUp(occupants)
    occupants = occupantSim.occupancyDown(occupants)
    print("Current occupancy count is", occupants)
    jsonReturn = json.dumps(occupancy, sort_keys=True, indent=4)
    print(jsonReturn)
    time.sleep(2)





