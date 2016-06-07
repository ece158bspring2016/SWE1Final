/*
 * DYEL_PIR_Arduino.ino
 *
 * [Description]
 * Controls 2 PIR sensors using an Arudino
 * Status of each sensor given by a green (ON) and red (OFF) LED
 * Reads input from Raspberry Pi
 * Sends sensor data to Raspberry Pi
 * Displays current readout to LCD
 *
 * [Information]
 * ECE 158B SP16 @ UCSD
 * Developed by Keith Choison
 * Created on June 4, 2016
 *
 */

/*
 * Configuration
 *
 * [Arduino]
 * ATmega 2560
 *
 * [Components]
 * 2 x PIR Sensors
 * 1 x LCD1602
 * 2 x Green LED
 * 2 x Red LED
 *
 * [Digital Pins]
 * 22 OUT - Red LED 2
 * 23 OUT - Green LED 2
 * 24 OUT - Green LED 1
 * 25 OUT - Red LED 1
 * 30 OUT - LiquidCrystal D7
 * 31 OUT - LiquidCrystal D6
 * 32 OUT - LiquidCrystal D5
 * 33 OUT - LiquidCrystal D4
 * 34 OUT - LiquidCrystal EN
 * 35 OUT - LiquidCrystal RS
 * 40 IN  - Raspberry Pi B GPIO1 (BCM18) / Raspberry Pi Status
 * 41 IN  - Raspberry Pi B GPIO3 (BCM22) / Input from PIR Sensor 1
 * 42 IN  - Raspberry Pi B GPIO4 (BCM23) / Input from PIR Sensor 2
 *
 */

#include <LiquidCrystal.h>

// define pin variables
int led1[] = {24, 25}; // 0 = Green, 1 = Red
int led2[] = {23, 22};
int piStatus = 40;
int pir1Sensor = 41;
int pir2Sensor = 42;

// define if Raspberry Pi has completed boot process
boolean piReady = false;

// define if LCD has been updated
boolean lcdUpdated = false;

// LiquidCrystal (RS, EN, D4, D5, D6, D7)
LiquidCrystal lcd (35, 34, 33, 32, 31, 30);

void setup (){
    // initialize serial port at 9600 baud
    Serial.begin (9600);

    // configure pins to their proper modes
    pinMode (led1[0], OUTPUT);
    pinMode (led1[1], OUTPUT);
    pinMode (led2[0], OUTPUT);
    pinMode (led2[1], OUTPUT);
    pinMode (piStatus, INPUT_PULLUP);
    pinMode (pir1Sensor, INPUT);
    pinMode (pir1Sensor, INPUT);

    // setup LCD and show "boot" screen
    lcd.begin (16, 2); // define 16 columns, 2 rows for LCD
    lcd.print ("DYEL by SWE");
    lcd.setCursor (0, 1); // set cursor to column 1, row 2
    lcd.print ("ECE 158B SP16");

    // wait 5 ms before showing waiting message
    delay (5000);

    // set initial states for LEDs
    digitalWrite (led1[0], HIGH);
    digitalWrite (led1[1], LOW);
    digitalWrite (led2[0], HIGH);
    digitalWrite (led2[1], LOW);
}

void loop (){
    // variables to store value of LEDs
    int led1Values[2];
    int led2Values[2];

    // read the current value of the LEDs
    led1Values[0] = digitalRead (led1[0]);
    led1Values[1] = digitalRead (led1[1]);
    led2Values[0] = digitalRead (led2[0]);
    led2Values[1] = digitalRead (led2[1]);

    if (!piReady){ // RPi is not ready yet
        // alternate LEDs while waiting for RPi to finish booting
        digitalWrite (led1[0], !led1Values[0]);
        digitalWrite (led1[1], !led1Values[1]);
        digitalWrite (led2[0], !led2Values[0]);
        digitalWrite (led2[1], !led2Values[1]);

        // show waiting message
        lcd.clear();
        lcd.print ("Please Wait...");

        // change lit up LED every second
        delay (1000);

        // see if RPi is ready
        piReady = (digitalRead (piStatus) == LOW);
    }else{ // RPi is ready!
        // read and store sensor values from RPi
        int pir1Status = digitalRead (pir1Sensor);
        int pir2Status = digitalRead (pir2Sensor);

        // update LEDs based on sensor values
        digitalWrite (led1[0], !pir1Status);
        digitalWrite (led1[1], pir1Status);
        digitalWrite (led2[0], !pir2Status);
        digitalWrite (led2[1], pir2Status);

        // update LCD to let user know RPi operational
        if (!lcdUpdated){
            lcd.clear();
            lcd.print ("Running...");
            lcdUpdated = true;
        }
    }
}
