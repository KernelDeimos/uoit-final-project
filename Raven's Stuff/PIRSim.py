import sensorSim, json, time, os, datetime, pytz, cbor

occupants = 0
temperature = 16.5
humidity = 45.5
count = 1

while True:
    currentTime = datetime.datetime.now(pytz.timezone('US/Eastern'))
    currentTimeString = currentTime.strftime('%m/%d/%y/%H/%M/%S')
    occupants = sensorSim.occupancyUp(occupants)
    occupants = sensorSim.occupancyDown(occupants)
    temperature = sensorSim.temperature(temperature)
    humidity = sensorSim.humidity(humidity)
    Environment = {'sensorData': {'SensorID': "Sensor1", 'Temperature': temperature, 'Humidity': humidity,
                   'Occupancy': occupants,'Time': currentTime}}
    jsonReturn = json.dumps(Environment, sort_keys=True, indent=4, default=str)
    cborReturn = cbor.dumps({'sensorData': {'SensorID': 'Sensor1', 'Temperature': temperature, 'Humidity': humidity,
                                            'Occupancy': occupants,'Time': currentTimeString}})
    cborReceive = cbor.loads(cborReturn)
    print("Sensor Reading", count)
    print(jsonReturn)
    print(cborReturn)
    print(cborReceive) #Putts cbor back to JSON
    count += 1
    time.sleep(2)



