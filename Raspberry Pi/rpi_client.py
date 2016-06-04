import time
import json

# Install Python-Firebase Library
# e.g. pip install -e git://github.com/mikexstudios/python-firebase.git#egg=python-firebase
from firebase import firebase

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
GPIO.setmode(GPIO.BOARD)


PIR_enter                = 0            # Input Pin for ENTER PIR Sensor
PIR_exit                 = 0            # Input Pin for EXIT PIR Sensor
PIRStatus                = None         # PIR Sensor HIGH/LOW output
occupancy_enter          = 0            # Variable for amount of people entering
occupancy_exit           = 0            # Variable for amount of people exiting
firebase_update_interval = 10           # Push to Firebase every X occupants
locations                = {'Main Gym', 'Rimac', 'Warren'}
destinated_location      = 0
firebase_URL             = str('https://ece158final.firebaseio.com/' + locations[destinated_location])
firebase_obj             = Firebase(firebase_URL)
date = time.strftime('%m/%d/%Y')

while (1):

    if date is not time.strftime('%m/%d/%Y'):
    # Push data to Firebase before resetting counters
        result = firebase_URL.put(data)
    # Reset occupancy every day
        occupancy_enter = 0
        occupancy_exit = 0

    # Wait (blocking) on GPIO Rise (Low to High)
    GPIO.add_event_detect(PIR_enter, GPIO.RISING)  # add rising edge detection on a channel
    GPIO.add_event_detect(PIR_exit, GPIO.RISING)  # add rising edge detection on a channel

    if GPIO.event_detected(PIR_enter):
        occupancy_enter += 1
    if GPIO.event_detected(PIR_exit):
        occupancy_exit += 1


    # Setup JSON for time, date, and current occupants
    data = {'Name': locations[destinated_location],
            'Time': time.strftime('%H:%M:%S'),
            'Date': time.strftime('%m/%d/%Y'),
            'Occupancy_Enter': occupancy_enter,
            'Occupancy_Exit': occupancy_exit,
            'Percentage_Occupied': str(float (occupancy_enter) / total_occupancy * 100) + '%'
           }

    # Push data to Firebase every X occupants
    if (occupancy_enter  % firebase_update_interval == 0) or (occupancy_exit % firebase_update_interval == 0):
        result = firebase_URL.put(data)
        print result


