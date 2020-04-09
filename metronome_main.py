#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time
import metronome_modes
import metronome_pulser

pins = [17, 18, 27, 22, 23, 24, 25, 13]
buttonPin = 26
MetModesDict = {0:"modeOff",1:"modeFlash", 2:"modeRegularLoop",3:"modeSlinky",4:"modeInsideOut"}
defaultMetMode = [0, MetModesDict[0]]
currentMetMode = defaultMetMode
#tempo = 100
tempoInSecPerBeep = 60. / 100
debugMode = False
'''DEBUG
print(MetModesDict)
print(defaultMetMode)
print(currentMetMode)
'''

def setup():
	GPIO.setmode(GPIO.BCM)        # Numbers GPIOs by BCM
	GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)    # Set buttonPin's mode is input, and pull up to high level(3.3V)
	for pin in pins:
		GPIO.setup(pin, GPIO.OUT)   # Set all pins' mode is output
		GPIO.output(pin, GPIO.HIGH) # Set all pins to high(+3.3V) to off led
	

		
def determine_next_mode(ev=None):
	currentMetMode[0] += 1 if currentMetMode[0] < (len(MetModesDict)-1)  else -(len(MetModesDict)-1) # reset to 0 if the next mode key is higher than the max in the dict
	if debugMode:#if debugging
		print(currentMetMode[0])
	currentMetMode[1] = MetModesDict[currentMetMode[0]] # define a list set to the current mode as defined in the dict - monitored by the cycler functions
	print("updated to " + str(currentMetMode))
	time.sleep(2)
		
def loop():
	GPIO.add_event_detect(buttonPin, GPIO.FALLING, callback=determine_next_mode, bouncetime=3000) # wait for falling and set bouncetime to prevent the callback function from being called multiple times when the button is pressed
	while True:
		if debugMode:#if debugging
			print("in main loop: " + str(currentMetMode))
		metronome_modes.modes_manager(currentMetMode, tempoInSecPerBeep)
		if debugMode:
			time.sleep(.5)
		

def destroy():
	metronome_pulser.destroy()		   # Stop pulser
	for pin in pins:
		GPIO.output(pin, GPIO.HIGH)    # turn off all leds
	GPIO.cleanup()                     # Release resource

if __name__ == '__main__':     # Program start from here
	setup()
	global tempoInSecPerBeep
	try:
		tempoInSecPerBeep = 60. / input("Tempo in bpm: ")
		print("Received tempo in Seconds: " + str(tempoInSecPerBeep))
		loop()
	except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
		destroy()

