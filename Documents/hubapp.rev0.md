# Hub Application (HA)

## HA/I2C
1. API: can recieve requests for data
2. API: "" Request update for sensor-actuator association upon sensor unit failure
   1. API: can revieve request to simulate sensor failure
3. HWI: can communicate via I2C
4. "" Recieves predefined I2C addressing upon start
   1. ? Maybe a config file has this
5. Makes sensors and actuators available to the manager
   (
    API to be determined. I'm thinking it'll make a named channel for each
    sensor or actuator and send SenML data through that channel.
   )
6. "" Sensor data saved in local buffer by I2C communication component

## HA/BLE
1. API: can recieve requests for data
2. API: "" Request update for sensor-actuator association upon sensor unit failure
3. API: can recieve request to reconfigure sensors
   1. i.e. broadcast address again and reconnect everything, for crit fails
4. HWI: communicats with sensors for data
   1. ? (poll, on request, or continuous listening)
5. ? HWI: can recieve a "kind of like a DHCP request" from a sensor
6. "" Broadcast address, ask for sensor units to register themselves, receive sensor-actuator association mapping
7. Understands sensor/actuator topology by breadth
   (i.e. sensors can be gateways to actuators, HA/BLE knows the correct gateway)

## HA/Manager
1. Starts the service for HA/Connective
2. "" Phase 1: Sends request for position change through I2C communication component which uses predefined I2C address
3. "" Phase 2: No difference from the HUB perspective, but request is propogated by governing sensor unit
4. "" Maintain a recent database of sensor readings and actuator positions
5. "" Provide saved data to the ML cloud server upon request
   1. Data can be downloaded from a locally available slack server
   2. Data is sent directly to cloud server based on IP address

## HA/Thermostat
1. Recieves instructions from manager
2. Manages A/C, Furnace, Fan directly
3. ? Maybe is part of manager
4. Handles manual overrides, communication with HestiaPi, etc

I'm thinking in Phase 1, HA/Thermostat is just part of HA/Manager, and in
phase 2 HA/Thermostat is decoupled, using "ericland" to get requests from
HA/Manager

## HA/Connective (AKA "ericland") - .so library with Python bindings
1. Exists within the shared library for communication (AKA "ericland")
2. Probably runs within the manager, i.e. the manager will call the function
   to start listening.

## HA/Util (AKA "ericlib") - .so library with Python bindings
1. Contains whatever utility functions people ask Eric to write
2. Has function to compress/decompress SenML's JSON representation
3. Unlike HA/Connective, this may exist on sensors and actuators
