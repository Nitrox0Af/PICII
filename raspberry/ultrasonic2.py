from gpiozero import DistanceSensor
from config import TRIG_PIN, ECHO_PIN
ultrasonic = DistanceSensor(echo=ECHO_PIN, trigger=TRIG_PIN)
while True:
    print(ultrasonic.distance)