import smbus2 #For i2c intercom from i2c out of sensors (hum and temp)
from gpiozero import MotionSensor #provides methods for easy use PIR
                                  #used for serial ttl signal from PIR thru
                                  #Pi GPIO

tempAddress = 0x?? #will be different when configured
               #represents i2c addy from sensor taking in temp when read
               #using i2cdetect -y 0
humAddress = 0x??
bus = smbus2.SMBus(0) #initialize i2c connection for data intake



def temperature():
    currentTemp = bus.read_byte_data(tempAddress, ?) #register param will depend
                                                  #on where coming from on bus
    temperature = int.from_bytes(currentTemp, byteorder="little")
    return temperature

def humidity():
    currentHum = bus.read_byte_data(humAddress, ?)
    humidity = int.from_bytes(currentHum, byteorder="little")
    return humidity

def occupancyUp():
    occupantcount = 0
    pir = MotionSensor(4)
    if pir.motion_detected():
        occupantcount += 1
        return occupantcount

def occupancyDown():
    occupantcount = 0
    pir = MotionSensor(4)
    if pir.motion_detected():
        occupantcount -= 1
        return occupantcount


