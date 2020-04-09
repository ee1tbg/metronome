#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time
import metronome_main

defaultPins = metronome_main.pins
tempPins = defaultPins
modeID = 0
lcurrentMetMode = [0,"modeOff"]
lpreviousMetMode = [0,"modeOff"]
firstRep = False
debugMode = metronome_main.debugMode
tempoInSecPerBeep = 100/60.

def modes_manager(currentMetModeFromMain, tempoInSecPerBeepFromMain):
	global lcurrentMetMode
	lcurrentMetMode = currentMetModeFromMain
	global lpreviousMetMode
	global firstRep
	global tempoInSecPerBeep
	tempoInSecPerBeep = tempoInSecPerBeepFromMain
	print("modes_manager tempo in Seconds: " + str(tempoInSecPerBeep))
	if debugMode:#if debugging
		print("lcurrentMetMode " + str(lcurrentMetMode))
		print("lpreviousMetMode " + str(lpreviousMetMode))
	firstRep = (lcurrentMetMode[0] is not lpreviousMetMode[0])
	if firstRep:	
		print("FIRST" + str(functionModeMap[1]))
	off()
	regular_loop()
	slinky()
	insideout()
	flashing()

	lpreviousMetMode = lcurrentMetMode

def off(pins = defaultPins):
	modeID = 0
	if debugMode:#if debugging
		print("in use: " + str(lcurrentMetMode))
	functionModeMap = [modeID, metronome_main.MetModesDict[modeID]]
	if lcurrentMetMode[0] is functionModeMap[0]:
		if firstRep:	
			print(functionModeMap[1])
		time.sleep(.1)
		
def flashing(pins = defaultPins):#flash all LEDS
	modeID = 1
	functionModeMap = [modeID, metronome_main.MetModesDict[modeID]]
	if lcurrentMetMode[0] is functionModeMap[0]:
		if firstRep:	
			print(functionModeMap[1])
		tempPins = defaultPins
		GPIO.output(tempPins,GPIO.LOW)
		#print("time on: " + str(tempoInSecPerBeep))
		time.sleep(tempoInSecPerBeep / 2.)
		GPIO.output(tempPins,GPIO.HIGH)
		#print("time on: " + str(tempoInSecPerBeep/2.))
		time.sleep(tempoInSecPerBeep / 2.)


def regular_loop(pins = defaultPins, override=False):
	modeID = 2
	functionModeMap = [modeID, metronome_main.MetModesDict[modeID]]
	if lcurrentMetMode[0] is functionModeMap[0] or override is True:
		if firstRep:	
			print(functionModeMap[1])
		tempPins = pins
		for pin in tempPins:
			GPIO.output(pin, GPIO.LOW)	
			time.sleep(tempoInSecPerBeep / len(pins) - .01)
			print("time on: " + str(tempoInSecPerBeep / len(pins) - .01))
			GPIO.output(pin, GPIO.HIGH)

def slinky(pins = defaultPins, override=False):
	modeID = 3
	functionModeMap = [modeID, metronome_main.MetModesDict[modeID]]
	if lcurrentMetMode[0] is functionModeMap[0] or override is True:
		if firstRep:	
			print(functionModeMap[1])
		tempPins = pins
		for pin in tempPins:
			GPIO.output(pin, GPIO.LOW)
			time.sleep(tempoInSecPerBeep / len(pins) / 2)
		for pin in tempPins:
			GPIO.output(pin, GPIO.HIGH)
			time.sleep(tempoInSecPerBeep / len(pins) / 2)
		
		tempPins = [pins[-i-1] for i in range(len(pins))]
		for pin in tempPins:
			GPIO.output(pin, GPIO.LOW)
			time.sleep(tempoInSecPerBeep / len(pins) / 2)
		for pin in tempPins:
			GPIO.output(pin, GPIO.HIGH)
			time.sleep(tempoInSecPerBeep / len(pins) / 2)
			
def insideout(pins = defaultPins):
	modeID = 4
	functionModeMap = [modeID, metronome_main.MetModesDict[modeID]]
	if lcurrentMetMode[0] is functionModeMap[0]:
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
		

