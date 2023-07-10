import RPi.GPIO as GPIO
import time
from config import TRIG_PIN, ECHO_PIN

class Ultrasonic:
    def __init__(self):
        self.trig_pin = TRIG_PIN
        self.echo_pin = ECHO_PIN

    def setup(self):
        """Setup the GPIO pins for the ultrasonic sensor."""
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.trig_pin, GPIO.OUT)
        GPIO.setup(self.echo_pin, GPIO.IN)

    def measure_distance(self):
        """Measure the distance using the ultrasonic sensor."""
        GPIO.output(self.trig_pin, GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(self.trig_pin, GPIO.LOW)

        pulse_start = 0
        pulse_end = 0

        while GPIO.input(self.echo_pin) == GPIO.LOW:
            pulse_start = time.time()

        while GPIO.input(self.echo_pin) == GPIO.HIGH:
            pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 34300 / 2

        return distance

    def cleanup(self):
        """Clean up the GPIO resources."""
        GPIO.cleanup()

if __name__ == '__main__':
    ultrasonic = Ultrasonic()
    ultrasonic.setup()

    distance = ultrasonic.measure_distance()
    print("Distância medida:", distance, "cm")

    ultrasonic.cleanup()
