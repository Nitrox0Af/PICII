
#! / usr / bin / python3
# Reed.py file
import time, sys
import RPi. GPIO as GPIO

PINO = 15
GPIO.setmode(GPIO.BOARD)
GPIO.setup(PINO, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
    input = GPIO.input(PINO)
    print (input)
    time.sleep (1)