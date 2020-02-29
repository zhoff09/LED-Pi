# File: ledcontrol.py
# Author: Zachary Hoffman
# Date: 2/29/2020
# Description:
# A python script that controls LEDs connected to a Raspberry Pi
# Uses spreadsheet to collect dates, and lights up specific LEDs on an anniversary



##############################
#         LIBRARIES          #
##############################

print ("Importing libraries...")
import time
import math
import board
import neopixel
from datetime import date, datetime, timedelta
from threading import Timer
import sys,tty,termios
import pandas as pd
import atexit



##############################
#         PARAMETERS         #
##############################

# LED information
LED_COUNT = 150
LED_PIN = board.D18

# colors: (G, R, B)
OFF_COLOR = (0, 0, 0)
DEFAULT_COLOR = (255, 255, 255)
ANIV_COLOR = (20, 255, 7)

# waits n seconds between each update
UPDATE_FREQ = 3600

# name of the Excel file containing Date/LED info
EXCEL_FILENAME = "Dates.xlsx"



##############################
#         FUNCTIONS          #
##############################

# updates LEDs with new date information
def Update():
    today = str(date.today())[5:]									# grabs today's date date
    print("\n~~~~~ Today's date:", today, "~~~~~\n")				# prints today's date
    
	# iterates through each row in spreadsheet
    print("Updating LEDs...")
	for i in range(LED_COUNT):
        led = data['LED #'][i]										# stores current row LED #
        day = str(data['Date'][i])[5:10]							# stores current row Date (mm-dd)

        if day == "":												# if current row has no date
            pixels[led] = OFF_COLOR									# set LED to OFF_COLOR
        elif day == today:											# if current row's date is an anniversary
            print("Found match: ", data['Name'][i],"- LED", led)	# indicate that a match was found
            pixels[led] = ANIV_COLOR								# set LED to ANIV_COLOR
        else:														# if current row's date is not an anniversary
            pixels[led] = DEFAULT_COLOR								# set LED to DEFAULT_COLOR
    
    pixels.show()													# update LEDs with new colors
    print("LEDs Updated!")

# executes when program is exited    
def exit_handler():
    pixels.fill(OFF_COLOR)											# sets LEDs to OFF_COLOR
    pixels.show()													# updates LEDs to turn them off
atexit.register(exit_handler)										# sets exit_handler() as method to use upon exit
    


##############################
#           DRIVER           #
##############################

print("Initializing LEDs...")										
pixels = neopixel.NeoPixel(LED_PIN, LED_COUNT)						# initializes array of LEDs w/ parameter info

print("Reading ", EXCEL_FILENAME, "...", sep="")
data = pd.read_excel(EXCEL_FILENAME)								# reads excel data into data variable

while True:															# run infinite loop
    Update()														# update LEDs
    print("Waiting", UPDATE_FREQ, "seconds...")
    time.sleep(UPDATE_FREQ)											# wait for UPDATE_FREQ seconds before next update