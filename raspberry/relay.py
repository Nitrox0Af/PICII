import time
import RPi.GPIO as GPIO
from config import RELAY_PIN, DELAY_RELAY

class Relay:
    def __init__(self, pin):
        self.pin = pin
        self.is_on = False

    def setup(self):
        """Set up the GPIO pin for the relay."""
        GPIO.setup(self.pin, GPIO.OUT)
        self.turn_off()

    def turn_on(self):
        """Turn on the relay."""
        GPIO.output(self.pin, GPIO.HIGH)
        self.is_on = True

    def turn_off(self):
        """Turn off the relay."""
        GPIO.output(self.pin, GPIO.LOW)
        self.is_on = False

    def toggle(self):
        """Toggle the state of the relay (turn on if off, turn off if on)."""
        if self.is_on:
            self.turn_off()
        else:
            self.turn_on()

    def cleanup(self):
        """Clean up the GPIO resources."""
        GPIO.cleanup()

def main():
    relay = Relay(RELAY_PIN)
    relay.setup()

    try:
        while True:
            relay.toggle()
            time.sleep(DELAY_RELAY)

    except KeyboardInterrupt:
        relay.cleanup()

if __name__ == '__main__':
    main()
