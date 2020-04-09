#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time
import LED_Cycler_main
from LED_Cycler_main import currentLedMode

defaultPins = LED_Cycler_main.pins
tempPins = defaultPins
modeID = 0
lcurrentLedMode = [0,"modeOff"]
lpreviousLedMode = [0,"modeOff"]
firstRep = False
debugMode = LED_Cycler_main.debugMode
tempoInSec = 100/60.

def modes_manager(currentLedModeFromMain, tempoInSecFromMain):
	global lcurrentLedMode
	lcurrentLedMode = currentLedModeFromMain
	global lpreviousLedMode
	global firstRep
	global tempoInSec
	tempoInSec = tempoInSecFromMain
	print("modes_manager tempo in Seconds: " + str(tempoInSec))
	if debugMode:#if debugging
		print("lcurrentLedMode " + str(lcurrentLedMode))
		print("lpreviousLedMode " + str(lpreviousLedMode))
	firstRep = (lcurrentLedMode[0] is not lpreviousLedMode[0])
	if firstRep:	
		print("FIRST" + str(functionModeMap[1]))
	off()
	regular_loop()
	slinky()
	insideout()
	flashing()

	lpreviousLedMode = lcurrentLedMode

def off(pins = defaultPins):
	modeID = 0
	if debugMode:#if debugging
		print("in use: " + str(lcurrentLedMode))
	functionModeMap = [modeID, LED_Cycler_main.ledModesDict[modeID]]
	if lcurrentLedMode[0] is functionModeMap[0]:
		if firstRep:	
			print(functionModeMap[1])
		time.sleep(.1)
		
def flashing(pins = defaultPins):#flash all LEDS
	modeID = 1
	functionModeMap = [modeID, LED_Cycler_main.ledModesDict[modeID]]
	if lcurrentLedMode[0] is functionModeMap[0]:
		if firstRep:	
			print(functionModeMap[1])
		tempPins = defaultPins
		GPIO.output(tempPins,GPIO.LOW)
		#print("time on: " + str(tempoInSec))
		time.sleep(tempoInSec / 2.)
		GPIO.output(tempPins,GPIO.HIGH)
		#print("time on: " + str(tempoInSec/2.))
		time.sleep(tempoInSec / 2.)


def regular_loop(pins = defaultPins, override=False):
	modeID = 2
	functionModeMap = [modeID, LED_Cycler_main.ledModesDict[modeID]]
	if lcurrentLedMode[0] is functionModeMap[0] or override is True:
		if firstRep:	
			print(functionModeMap[1])
		tempPins = pins
		for pin in tempPins:
			GPIO.output(pin, GPIO.LOW)	
			time.sleep(tempoInSec / len(pins) - .01)
			print("time on: " + str(tempoInSec / len(pins) - .01))
			GPIO.output(pin, GPIO.HIGH)

def slinky(pins = defaultPins, override=False):
	modeID = 3
	functionModeMap = [modeID, LED_Cycler_main.ledModesDict[modeID]]
	if lcurrentLedMode[0] is functionModeMap[0] or override is True:
		if firstRep:	
			print(functionModeMap[1])
		tempPins = pins
		for pin in tempPins:
			GPIO.output(pin, GPIO.LOW)
			time.sleep(tempoInSec / len(pins) / 2)
		for pin in tempPins:
			GPIO.output(pin, GPIO.HIGH)
			time.sleep(tempoInSec / len(pins) / 2)
		
		tempPins = [pins[-i-1] for i in range(len(pins))]
		for pin in tempPins:
			GPIO.output(pin, GPIO.LOW)
			time.sleep(tempoInSec / len(pins) / 2)
		for pin in tempPins:
			GPIO.output(pin, GPIO.HIGH)
			time.sleep(tempoInSec / len(pins) / 2)
			
def insideout(pins = defaultPins):
	modeID = 4
	functionModeMap = [modeID, LED_Cycler_main.ledModesDict[modeID]]
	if lcurrentLedMode[0] is functionModeMap[0]:
		if firstRep:	
			print(functionModeMap[1])
		# First define new pin list
		middleLedIndex = len(pins)/2 - 1
		tempPins = []
	
		#print(middleLedIndex)
		prevLedIndex = middleLedIndex
		# 0  1  2  3  4  5  6  7 : default pin index (and i)
		# 3  4  2  5  1  6  0  7 : default pin index within temp pins
		# 0 +1 -2 +3 -4 +5 -6 +7 : change in default pin index
		for i in range(len(defaultPins)):
			newLedIndex = prevLedIndex - (i * ((-1)**i))
			tempPins.append(defaultPins[newLedIndex])
		
			''' DEBUG
			print(i, prevLedIndex, newLedIndex)
			print(((-1)**i), -(i * ((-1)**i)))
			print(tempPins[i], tempPins, defaultPins)
			print("")
			'''
			#GPIO.output(tempPins, GPIO.LOW)	
			#time.sleep(0.05)
		
			prevLedIndex = newLedIndex
		#print(defaultPins)
		#print(tempPins)
		#GPIO.output(tempPins, GPIO.HIGH)
	
		#regular_loop(tempPins, True)
		slinky(tempPins, True)
		

