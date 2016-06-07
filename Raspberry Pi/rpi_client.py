import time
import json

# Install Python-Firebase Library
# e.g. pip install -e git://github.com/mikexstudios/python-firebase.git#egg=python-firebase
from firebase import Firebase

# Raspberry Pi Python GPIO Library
# https://pypi.python.org/pypi/RPi.GPIO
# Install Python-GPIO
# e.g. $ sudo pip install hg+http://hg.code.sf.net/p/raspberry-gpio-python/code#egg=RPi.GPIO
try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO!  "
          "This is probably because you need superuser privileges.  "
          "You can achieve this by using 'sudo' to run your script")

GPIO.setwarnings(False)

# Set RPi GPIO numbering system to Broadcom SOC Channel
GPIO.setmode(GPIO.BCM)

RPi_status_output = 18 # Output Pin for Raspberry Pi Status
PIR_enter_input = 4 # Input Pin for ENTER PIR Sensor
PIR_enter_output = 22 # Output Pin for ENTER PIR sensor (to Arduino)
PIR_exit_input = 24 # Input Pin for EXIT PIR Sensor
PIR_exit_output = 23 # Output Pin for EXIT PIR Sensor (to Arduino)

GPIO.setup(RPi_status_output, GPIO.OUT) # Setup RPi_status_output pin as OUTPUT pin
GPIO.setup(PIR_enter_input, GPIO.IN) # Setup PIR_enter_input pin as INPUT pin
GPIO.setup(PIR_enter_output, GPIO.OUT, initial=GPIO.LOW) # Setup PIR_enter_output pin as OUTPUT pin
GPIO.setup(PIR_exit_input, GPIO.IN) # Setup PIR_exit_input pin as INPUT pin
GPIO.setup(PIR_exit_output, GPIO.OUT, initial=GPIO.LOW) # Setup PIR_exit_output pin as OUTPUT pin

GPIO.add_event_detect(PIR_enter_input, GPIO.RISING) # add rising edge detection on a channel
GPIO.add_event_detect(PIR_exit_input, GPIO.RISING) # add rising edge detection on a channel

occupancy_enter = 0 # Variable for amount of people entering
occupancy_exit = 0 # Variable for amount of people exiting
total_occupancy = 200
firebase_update_interval = 1 # Push to Firebase every X occupants
locations = ['Main Gym', 'Rimac', 'Warren'] # Contain list of locations
destinated_location = 0 # Destinated location
firebase_URL = str('https://ece158final.firebaseio.com/') + locations[destinated_location]
firebase_obj = Firebase(firebase_URL) # Firebase object for sending HTTP requests
date = time.strftime('%m/%d/%Y') # Initialize time variable
data = None # Declare data variable

try:
    while True:
        # Let Arduino know that Raspberry Pi has connected to Firebase and is ready
        GPIO.output(RPi_status_output, GPIO.HIGH)

        if date is not time.strftime('%m/%d/%Y'):
            # Push data to Firebase before resetting counters
            result = firebase_obj.put(data)
            # Reset occupancy every day
            # occupancy_enter = 0
            # occupancy_exit = 0

        # Increment enter counter if PIR_enter sensor sends digital HIGH (person detected)
        if GPIO.event_detected(PIR_enter_input):
            occupancy_enter += 1
            GPIO.output(PIR_enter_output, GPIO.HIGH) # Let Arduino know PIR_enter sensor triggered
        else:
            GPIO.output(PIR_enter_output, GPIO.LOW) # Let Arduino know PIR_enter sensor detected nothing

        # Increment exit counter if PIR_exit sensor sends digital HIGH (nothing detected)
        if GPIO.event_detected(PIR_exit_input):
            occupancy_exit += 1
            GPIO.output(PIR_exit_output, GPIO.HIGH) # Let Arduino know PIR_exit sensor triggered
        else:
            GPIO.output(PIR_exit_output, GPIO.LOW) # Let Arduino know PIR_exit sensor detected nothing

        # Push data to Firebase every X occupants
        if (occupancy_enter  % firebase_update_interval == 0) or (occupancy_exit % firebase_update_interval == 0):
            # Setup JSON for time, date, and current occupants
            data = {'Name': locations[destinated_location],
                'Time': time.strftime('%H:%M:%S'),
                'Date': time.strftime('%m/%d/%Y'),
                'Occupancy_Enter': occupancy_enter,
                'Occupancy_Exit': occupancy_exit,
                'Percentage_Occupied': str(float (occupancy_enter) / total_occupancy * 100) + '%'
               }
            result = firebase_obj.put(data)
            print result
except KeyboardInterrupt:
    GPIO.cleanup()

# Clean up GPIO pin allocation
GPIO.cleanup()
