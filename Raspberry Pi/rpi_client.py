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


# Set RPi GPIO numbering system
GPIO.setmode(GPIO.BCM)

PIR_enter                = 4            # Input Pin for ENTER PIR Sensor
PIR_exit                 = 5            # Input Pin for EXIT PIR Sensor
GPIO.setup(PIR_enter, GPIO.IN)          # Setup PIR_enter pin as INPUT pin
GPIO.setup(PIR_exit, GPIO.IN)           # Setup PIR_exit pin as INPUT pin
GPIO.add_event_detect(PIR_enter, GPIO.RISING)  # add rising edge detection on a channel
GPIO.add_event_detect(PIR_exit, GPIO.RISING)   # add rising edge detection on a channel
occupancy_enter          = 0            # Variable for amount of people entering
occupancy_exit           = 0            # Variable for amount of people exiting
total_occupancy          = 200
firebase_update_interval = 10           # Push to Firebase every X occupants
locations                = ['Main Gym', 'Rimac', 'Warren'] # Contain list of locations
destinated_location      = 0                               # Destinated location
firebase_URL             = str('https://ece158final.firebaseio.com/') + locations[destinated_location]
firebase_obj             = Firebase(firebase_URL)   # Firebase object for sending HTTP requests
date = time.strftime('%m/%d/%Y')                    # Initialize time variable
data = None                                         # Declare data var.

while (1):
    if date is not time.strftime('%m/%d/%Y'):
        # Push data to Firebase before resetting counters
        result = firebase_obj.put(data)
        # Reset occupancy every day
        occupancy_enter = 0
        occupancy_exit = 0

    # Increment counter if either Pi detect digital HIGH input
    if GPIO.event_detected(PIR_enter):
        occupancy_enter += 1
    if GPIO.event_detected(PIR_exit):
        occupancy_exit += 1

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

# Clean up GPIO pin allocation
GPIO.cleanup()