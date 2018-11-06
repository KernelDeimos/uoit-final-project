import json
#import RPi.GPIO as GPIO
import time
import random

sensorName = "PIR Sensor"
i = 1                           #i=GPIO.input(11)
j = 0                           #j=GPIO.input(12)
occupants = 0

while True:
    i = random.randint(0,1)
    j = random.randint(0,1)
    if i == 0 and j == 0:
        print("No one is here.")
    elif i == 1 and j == 0:
        print("Saw someone coming from the left")
        occupants += 1
    elif i == 0 and j == 1:
        print("Saw someone coming from the right")
        if occupants > 0:
            occupants -= 1
    elif i == 1 and j == 1:
        print("Someone is in the middle.")

    data = {'sensorData': {'SensorID': sensorName, 'Occupants': occupants}}

    print(json.dumps(data, sort_keys=True, indent=4))

