import random
import time

def temperature(temperature):
    chance = random.randint(0, 5)
    if chance == 3:
        temperature += .1
        return temperature
    if chance == 4:
        temperature -= .1
        return temperature
    else:
        return temperature

def humidity(humidity):
    chance = random.randint(0, 5)
    if chance == 3:
        humidity += .1
        return humidity
    if chance == 4:
        humidity -= .1
        return humidity
    else:
        return humidity

def occupancyUp(currentOccupants):
    pir1 = random.randint(0, 1)

    if currentOccupants == 3:
        return currentOccupants
    elif pir1 == 1:
        pir2 = random.randint(0, 1)
        if pir2 == 1:
            print(" ")
            print("Someone entered the room.")
            print(" ")
            time.sleep(2)
            occupantCount = currentOccupants
            occupantCount += 1
            return occupantCount
        else:
            occupantCount = currentOccupants
            return occupantCount
        return currentOccupants
    else:
        return currentOccupants

def occupancyDown(currentOccupants):
    pir2 = random.randint(0, 1)
    if currentOccupants == 0:
        return currentOccupants
    elif pir2 == 1:
        pir1 = random.randint(0, 1)
        if pir1 == 1:
            print(" ")
            print("Someone left the room.")
            print(" ")
            time.sleep(2)
            occupantCount = currentOccupants
            occupantCount -= 1
            return occupantCount
        else:
            occupantCount = currentOccupants
            return occupantCount
        return currentOccupants
    else:
        return currentOccupants