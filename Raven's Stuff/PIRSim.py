import sensorSim
import json
import time
import os

occupants = 0
temperature = 16.5
humidity = 45.5
count = 1

while True:
    occupants = sensorSim.occupancyUp(occupants)
    occupants = sensorSim.occupancyDown(occupants)
    temperature = sensorSim.temperature(temperature)
    humidity = sensorSim.humidity(humidity)
    Environment = {'sensorData': {'SensorID': "Sensor1", 'Temperature': temperature, 'Humidity': humidity,
                   'Occupancy': occupants}}
    jsonReturn2 = json.dumps(Environment, sort_keys=True, indent=4)
    print("Sensor Reading", count)
    print(jsonReturn2)
    count += 1
    time.sleep(2)



