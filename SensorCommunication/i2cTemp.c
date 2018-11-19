/*Functioning to recognize addressing of ds1631 i2c termperature sensors and read
accurate temperature sensing. Will soon work for HIH7120 humdity sensor as well
Needs to be included in linked function call from python scripting implementation once
finalized. Will also need to be integrated as part of a hierarchical i2c mcp23017 bus
scripting implementing modular capacity for i2c temperature and humidity sensors*/

#include <stdio.h>
#include <wiringPiI2C.h>

float getTemperature(int fd)
{
	/* Start Start Temperature Conversion */
	int convert = wiringPiI2CWrite(fd, 0x51);
	/* Read from Temperature Registry 0xAA */
	int raw = wiringPiI2CReadReg16(fd, 0xAA);
	/* Perform Temparture Conversion to Celsius */
	raw = ((raw << 8) & 0xFF00) + (raw >> 8);
	return (float)((raw / 32.0) / 8.0);
}

int main(int argc, char *argv[])
{
	/* Sensor Address */
	int address = 0x48;

	/* Read from I2C and print temperature */
	int fd = wiringPiI2CSetup(address);
	printf("%.2f\n", getTemperature(fd) );
	return 0;
}
