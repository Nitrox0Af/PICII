#!/usr/bin/env python3          
                                
import signal                   
import sys
import RPi.GPIO as GPIO
from config import BUTTON_PIN

def signal_handler(sig, frame):
    GPIO.cleanup()
    sys.exit(0)

def button_callback(channel):
    if GPIO.input(BUTTON_PIN):
        print("Button released!")
    else:
        print("Button pressed!") 

if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)
    
    GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  

    GPIO.add_event_detect(BUTTON_PIN, GPIO.BOTH, callback=button_callback, bouncetime=50)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.pause()