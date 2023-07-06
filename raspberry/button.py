import time
import RPi.GPIO as GPIO
from config import BUTTON_PIN

class Button:
    def __init__(self, pin):
        self.pin = pin
        self.last_state = GPIO.HIGH
        self.last_change_time = time.time()

    def setup(self):
        """Setup the GPIO pin for the button."""
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def is_pressed(self):
        """Check if the button is pressed."""
        current_state = GPIO.input(self.pin)
        current_time = time.time()

        if current_state != self.last_state:
            self.last_change_time = current_time

        if current_time - self.last_change_time >= 0.05:  # Debounce time of 50 ms
            if current_state == GPIO.LOW:
                self.last_state = current_state
                return True

        self.last_state = current_state
        return False

    def cleanup(self):
        """Clean up the GPIO resources."""
        GPIO.cleanup()

def main():
    button = Button(BUTTON_PIN)
    button.setup()

    try:
        while True:
            if button.is_pressed():
                print("Button pressed!")

    except KeyboardInterrupt:
        button.cleanup()

if __name__ == '__main__':
    main()
