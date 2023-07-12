import time
import RPi. GPIO as GPIO
from config import REED_SENSOR_PIN

def setup():
    GPIO.setup(REED_SENSOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def get_input():
    input_reed = GPIO.input(REED_SENSOR_PIN)
    return input_reed

def main():
    GPIO.setmode(GPIO.BCM)
    setup()
    while True:
        input_reed = get_input()
        print(input_reed)
        time.sleep(1)

if __name__ == '__main__':
    main()