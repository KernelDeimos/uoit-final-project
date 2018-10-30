# HA/Connective

This is the connective component for the hub application.

The connective component creates an abstract model for IoT devices, and in
particular the sensor-actuator nodes for HVAC control. This component is
implemented as a shared library. (.so for Linux target, .dll in Windows)
This allows interoperability between components written in different
programming languages, including Python, Javascript, C, Golang, and more.

Bindings will be written for Python, our main development language for other
components, and may be written for other languages in the future if deemed
useful.

## Features Planned
- Create data structures, including lists and request queues
- Share these resources over HTTP
- Check requests queues with either non-blocking or blocking calls
- Two APIs: low-level (from C bindings), and high-level (from Python bindings)
- High-level functions in Python bindings for HVAC-specific use case

## Stretch Goals
- Share resources over simpler TCP protocol (eliminate overhead of HTTP)
- Implement security roles in case a component is compromised

## API Documentation

## Low-Level API

### `uint64 elconn_init(int32 mode)`

Initializes the library. Calling this function is required before using any
other library function.

The value of `mode` determins the library's behaviour as follows:
- value of `0`: perform normal operation
- value of `1`: perform normal operation, and display debug messages
