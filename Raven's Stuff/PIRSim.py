import sensorSim
import json
import time
import os

occupants = 0
temperature = 16.5
humidity = 45

while True:
    occupants = sensorSim.occupancyUp(occupants)
    occupants = sensorSim.occupancyDown(occupants)
    temperature = sensorSim.temperature(temperature)
    Occupancy = {'sensorData': {'SensorID': "PIR1", 'Occupants': occupants}}
    Environment = {'sensorData': {'SensorID': "TH1", 'Temperature': temperature, 'Humidity': humidity}}
    jsonReturn1 = json.dumps(Occupancy, sort_keys=True, indent=4)
    jsonReturn2 = json.dumps(Environment, sort_keys=True, indent=4)
    print(jsonReturn1)
    print(jsonReturn2)
    time.sleep(2)



