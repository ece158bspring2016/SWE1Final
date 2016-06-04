# DYEL (Midterm Project)
by Software Engineers (SWE)

## Overview
The midterm project provides the baseline functionality of reading from a sensor using an Arduino that is connected to the Internet via Raspberry Pi. The temperature readout is then pushed by the Raspberry Pi to Firebase (which we use as the BaaS) via Python (using the REST API) and is read by the iPhone application.

We use a temperature sensor in this project to demonstrate the working networking capabilities of pushing data from a sensor to the end user. For the final project, we will replace the temperature sensor with pyroelectric infrared (PIR) sensors to detect how many people are in a room at a given time.

## Components
There are multiple components that drive the functionality of our project. A brief overview of each is explained in the sections that follow.

#### iPhone
The Xcode project file is stored within the `root` directory of this repo.

The application is written in the Swift programming language using Xcode 7.3. It simply reads from the Firebase BaaS and displays the current temperature to the end user in real time.

#### Firebase
We use the Firebase as the BaaS that the Raspberry Pi writes to and the iPhone app reads from. See the respective sections for a more detailed overview.

#### Arduino
The `*.ino` code that powers the Arduino is stored within the `arduino` directory of this repo.

The code is designed for use on the Arduino 2560 Mega board and utilizes the following pins:
* Analog In: `A0`  
  This is where the data line from the `KY013` temperature sensor connects to. The sensor uses a thermistor (a variable resistor based on temperature) and the code calculates the changes in voltage to determine the current temperature.
* Digital Out: `44`, `46`, `50`, `51`, `52`, `53`  
  These pins are for the `LCD1602` display (driven by a Hitachi `HD44780` chipset) using the `LiquidCrystal` library to display the current readout of the temperature sensor (which is used for display purposes only).

The Arduino also writes the data to its serial port using a rate of 9600 baud every 500 milliseconds.

#### Raspberry Pi
The Pi is primarily responsible for providing Internet connectivity to the Arduino by pushing the sensor data to Firebase. The `*.py` script is located in the `python` directory of this repo.

The Arduino is connected to the the Pi via USB. The Python script reads from `/dev/ttyACM0` of the Pi (which the Arduino writes the serial data to) and updates this data using the `python-firebase` library by ozgur (available [here](http://ozgur.github.io/python-firebase/)).

------
ECE 158B SP16

SWE is Sara Farsi, Max Xing, Erik Xu, and Keith Choison.
