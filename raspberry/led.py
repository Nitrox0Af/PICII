import RPi.GPIO as GPIO
from config import LED_PIN

class LED:
    def __init__(self, pin):
        self.pin = pin
        self.is_on = False

    def setup(self):
        """Setup the GPIO pin for the LED."""
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        self.turn_off()

    def turn_on(self):
        """Turn on the LED."""
        GPIO.output(self.pin, GPIO.HIGH)
        self.is_on = True

    def turn_off(self):
        """Turn off the LED."""
        GPIO.output(self.pin, GPIO.LOW)
        self.is_on = False

    def toggle(self):
        """Toggle the state of the LED."""
        if self.is_on:
            self.turn_off()
        else:
            self.turn_on()

    def cleanup(self):
        """Clean up the GPIO resources."""
        GPIO.cleanup()

def main():
    led = LED(LED_PIN)
    led.setup()

    try:
        while True:
            led.toggle()

    except KeyboardInterrupt:
        led.cleanup()

if __name__ == '__main__':
    main()
