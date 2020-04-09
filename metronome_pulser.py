#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time
import metronome_main

LedPin = 18

def setup():
	global p
	GPIO.setmode(GPIO.BCM)       # Numbers GPIOs by BCM
	GPIO.setup(LedPin, GPIO.OUT)   # Set LedPin's mode is output
	GPIO.output(LedPin, GPIO.LOW)  # Set LedPin to low(0V)

	p = GPIO.PWM(LedPin, 1000)     # set Frequece to 1KHz
	p.start(0)                     # Duty Cycle = 0

def loop():
        secondToIncrement = 100
        tempoBPM = 120.
        tempoSPB = 60. / tempoBPM
        timeOn = tempoSPB / 100. # in sec
        percentPWIcrementOn = timeOn * secondToIncrement
        timeOff = tempoSPB / 100. # in sec
        percentPWIcrementOff = timeOff * secondToIncrement
        
	while True:
		for dc in range(0, 101, 20):   # Increase duty cycle: 0~100
			p.ChangeDutyCycle(dc)     # Change duty cycle
			time.sleep(0.05)
		time.sleep(.1)
		for dc in range(100, -1, -5): # Decrease duty cycle: 100~0
			p.ChangeDutyCycle(dc)
			time.sleep(0.05)
		time.sleep(.1)

def destroy():
	p.stop()
