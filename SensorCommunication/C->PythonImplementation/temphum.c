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

#include <wiringPi.h>  
#include <stdio.h>  
#include <stdlib.h>  
#include <stdint.h>  
#define MAX_TIME 85  
#define DHT11PIN 4  
int dht11_val[5]={0,0,0,0,0};  
  
void dht11_read_val()  
{  
  uint8_t lststate=HIGH;  
  uint8_t counter=0;  
  uint8_t j=0,i;  
  float farenheit;  
  for(i=0;i<5;i++)  
     dht11_val[i]=0;  
  pinMode(DHT11PIN,OUTPUT);  
  digitalWrite(DHT11PIN,LOW);  
  delay(18);  
  digitalWrite(DHT11PIN,HIGH);  
  delayMicroseconds(40);  
  pinMode(DHT11PIN,INPUT);  
  for(i=0;i<MAX_TIME;i++)  
  {  
    counter=0;  
    while(digitalRead(DHT11PIN)==lststate){  
      counter++;  
      delayMicroseconds(1);  
      if(counter==255)  
        break;  
    }  
    lststate=digitalRead(DHT11PIN);  
    if(counter==255)  
       break;  
    // top 3 transistions are ignored  
    if((i>=4)&&(i%2==0)){  
      dht11_val[j/8]<<=1;  
      if(counter>16)  
        dht11_val[j/8]|=1;  
      j++;  
    }  
  }  
  // verify cheksum and print the verified data  
  if((j>=40)&&(dht11_val[4]==((dht11_val[0]+dht11_val[1]+dht11_val[2]+dht11_val[3])& 0xFF)))  
  {  
    farenheit=dht11_val[2]*9./5.+32;  
    printf("Humidity = %d.%d %% Temperature = %d.%d *C (%.1f *F)\n",dht11_val[0],dht11_val[1],dht11_val[2],dht11_val[3],farenheit);  
  }  
  else  
    printf("Invalid Data!!\n");  
}  

int main(int argc, char *argv[])
{
	int address1 = 0x48;
	int address2 = 0x49;
	//if (1 < argc)
	//{
	//	address = (int)strtol(argv[1], NULL, 0);
	//}
//	signal(SIGINT, sigint_handler);
	if (wiringPiSetup()==-1) exit(1);
	/* Read from I2C and print temperature */
	int fd1 = wiringPiI2CSetup(address1);
	int fd2 = wiringPiI2CSetup(address2);
	usleep(125000);
	for(;;) {
		t1 = getTemperature(fd1);
		usleep(750000);
		t2 = getTemperature(fd2);
		sigint_handler();
		dht11_read_val();
	}
	return 0;
}

void sigint_handler() {
	printf("%.2f,%.2f\n", t1, t2);
	fflush(stdout);
	return;
}
