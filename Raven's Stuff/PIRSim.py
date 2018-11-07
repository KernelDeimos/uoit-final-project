import sensorSim, json, time, os, datetime, pytz

occupants = 0
temperature = 16.5
humidity = 45.5
count = 1

while True:
    currentTime = datetime.datetime.now(pytz.timezone('US/Eastern'))
    occupants = sensorSim.occupancyUp(occupants)
    occupants = sensorSim.occupancyDown(occupants)
    temperature = sensorSim.temperature(temperature)
    humidity = sensorSim.humidity(humidity)
    Environment = {'sensorData': {'SensorID': "Sensor1", 'Temperature': temperature, 'Humidity': humidity,
                   'Occupancy': occupants,'Time': currentTime}}
    jsonReturn2 = json.dumps(Environment, sort_keys=True, indent=4, default=str)
    print("Sensor Reading", count)
    print(jsonReturn2)
    count += 1
    time.sleep(2)



