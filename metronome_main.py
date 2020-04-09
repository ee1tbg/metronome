#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time
import LED_Cycler_modes

pins = [17, 18, 27, 22, 23, 24, 25, 13]
buttonPin = 26
ledModesDict = {0:"modeOff",1:"modeFlash", 2:"modeRegularLoop",3:"modeSlinky",4:"modeInsideOut"}
defaultLedMode = [0, ledModesDict[0]]
currentLedMode = defaultLedMode
#tempo = 100
tempoInSec = 60. / 100
debugMode = False
'''DEBUG
print(ledModesDict)
print(defaultLedMode)
print(currentLedMode)
'''

def setup():
	GPIO.setmode(GPIO.BCM)        # Numbers GPIOs by BCM
	GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)    # Set buttonPin's mode is input, and pull up to high level(3.3V)
	for pin in pins:
		GPIO.setup(pin, GPIO.OUT)   # Set all pins' mode is output
		GPIO.output(pin, GPIO.HIGH) # Set all pins to high(+3.3V) to off led
	

		
def determine_next_mode(ev=None):
	currentLedMode[0] += 1 if currentLedMode[0] < (len(ledModesDict)-1)  else -(len(ledModesDict)-1) # reset to 0 if the next mode key is higher than the max in the dict
	if debugMode:#if debugging
		print(currentLedMode[0])
	currentLedMode[1] = ledModesDict[currentLedMode[0]] # define a list set to the current mode as defined in the dict - monitored by the cycler functions
	print("updated to " + str(currentLedMode))
	time.sleep(2)
		
def loop():
	GPIO.add_event_detect(buttonPin, GPIO.FALLING, callback=determine_next_mode, bouncetime=3000) # wait for falling and set bouncetime to prevent the callback function from being called multiple times when the button is pressed
	while True:
		if debugMode:#if debugging
			print("in main loop: " + str(currentLedMode))
		LED_Cycler_modes.modes_manager(currentLedMode, tempoInSec)
		if debugMode:
			time.sleep(.5)
		

def destroy():
	for pin in pins:
		GPIO.output(pin, GPIO.HIGH)    # turn off all leds
	GPIO.cleanup()                     # Release resource

if __name__ == '__main__':     # Program start from here
	setup()
	global tempoInSec
	try:
		tempoInSec = 60. / input("Tempo in bpm: ")
		print("Received tempo in Seconds: " + str(tempoInSec))
		loop()
	except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
		destroy()

