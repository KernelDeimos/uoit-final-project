#include <stdio.h>
#include <wiringPiI2C.h>
#include <unistd.h>
#include <time.h>
#include <signal.h>

void sigint_handler();

float t1=0, t2=0;

float getTemperature(int fd)
{
	int convert = wiringPiI2CWrite(fd, 0x51);
	char str[32];
	sprintf(str, "DO SOMETHING: %d", convert);
	int raw = wiringPiI2CReadReg16(fd, 0xAA);
	raw = ((raw << 8) & 0xFF00) + (raw >> 8);
	return (float)((raw / 32.0) / 8.0);
}

int main(int argc, char *argv[])
{
	int address1 = 0x48;
	int address2 = 0x49;
	//if (1 < argc)
	//{
	//	address = (int)strtol(argv[1], NULL, 0);
	//}
	signal(SIGINT, sigint_handler);
	/* Read from I2C and print temperature */
	int fd1 = wiringPiI2CSetup(address1);
	int fd2 = wiringPiI2CSetup(address2);
	usleep(125000);
	for(;;) {
		t1 = getTemperature(fd1);
		usleep(750000);
		t2 = getTemperature(fd2);
		sigint_handler();
	}
	return 0;
}

void sigint_handler() {
	printf("%.2f,%.2f\n", t1, t2);
	fflush(stdout);
	return;
}
