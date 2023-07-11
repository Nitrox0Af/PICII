from gpiozero import DistanceSensor
from config import TRIG_PIN, ECHO_PIN

def hello():
    print("Hello")

def bye():
    print("Bye")

ultrasonic = DistanceSensor(echo=ECHO_PIN, trigger=TRIG_PIN, threshold_distance=0.5, max_distance=2)

ultrasonic.when_in_range = hello

ultrasonic.when_out_of_range = bye

while True:
    print(ultrasonic.distance)
