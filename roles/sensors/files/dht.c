/*
 *  dht.c:
 *	read temperature and humidity from DHT11 or DHT22 sensor
 *
 * depends on 'wiringpi' apt package
 * based on:  http://www.uugear.com/portfolio/read-dht1122-temperature-humidity-sensor-from-raspberry-pi/
 *
 * wiring pi layout: http://wiringpi.com/pins/

 */

#include <wiringPi.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

#define MAX_TIMINGS	85
#define MAX_TRIES	5

int data[5] = { 0, 0, 0, 0, 0 };

int print_json(int dht_pin) {
    uint8_t laststate	= HIGH;
    uint8_t counter	= 0;
    uint8_t j	        = 0, i;

    data[0] = data[1] = data[2] = data[3] = data[4] = 0;

    /* pull pin down for 18 milliseconds */
    pinMode(dht_pin, OUTPUT);
    digitalWrite(dht_pin, LOW);
    delay(18);

    /* prepare to read the pin */
    pinMode(dht_pin, INPUT);
    //printf("%i\n", laststate);

    /* detect change and read data */
    for (i = 0; i < MAX_TIMINGS; i++) {
        counter = 0;

        while (digitalRead(dht_pin) == laststate ) {
            counter++;
            delayMicroseconds(1);
            if (counter == 255)  {
                //printf("inner 255 at %i\n", i);
                break;
            }
        }
        laststate = digitalRead(dht_pin);

        if (counter == 255) {
            break;
        }

        /* ignore first 3 transitions */
        if ( (i >= 4) && (i % 2 == 0) ) {
            /* shove each bit into the storage bytes */
            data[j / 8] <<= 1;
            if (counter > 16) {
                data[j / 8] |= 1;
            }
            j++;
        }
    }

    /*
     * check we read 40 bits (8bit x 5 ) + verify checksum in the last byte
     * print it out if data is good
     */
    if ( (j>=40) && (data[4] == ((data[0]+data[1]+data[2]+data[3]) & 0xFF)) ) {
        float h = (float)((data[0] << 8) + data[1]) / 10;
        if (h > 100) {
            h = data[0];	// for DHT11
        }
        float c = (float)(((data[2] & 0x7F) << 8) + data[3]) / 10;
        if (c > 125) {
            c = data[2];	// for DHT11
        }
        if (data[2] & 0x80) {
            c = -c;
        }
        printf("{\"humidity\": %.1f, \"temp\": %.1f, \"dht_pin\": %d}\n", h, c, dht_pin);
       return 0;
    } else  {
        // printf("{\"error\": \"checksum\"}\n" );
        return 1;
    }
}

int main(int argc, char* argv[]) {
    if (wiringPiSetup() == -1) {
        printf("{\"error\": \"please install wiringPi\"}\n" );
        exit(1);
    }

    // defaulting to pin 3
    // in wiringPi, dht_pin 3 is GPIO-22
    // reference: http://wiringpi.com/pins/
    int dht_pin = 3;
    if (argc == 2) {
        // read first argument and try to parse as string

        if (sscanf(argv[1], "%i", &dht_pin) != 1) {
            printf("{\"error\": \"parsing DHT_PIN failed\"}\n");
            exit(3);
        }
    } else if (argc != 1) {
        printf("{\"error\": \"usage: ./dht [DHT_PIN]\"}\n" );
        exit(2);
    }

    int i;
    int dht_res = 1;
    while (dht_res !=0 && i < MAX_TRIES) {
        delay(2000);
        dht_res = print_json(dht_pin);
        i++;
    }

    if (dht_res != 0) {
        printf("{\"error\": \"no valid data\", \"dht_pin\": %d}\n", dht_pin);
    }

    return(dht_res);
}
