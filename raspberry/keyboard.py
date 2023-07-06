import RPi.GPIO as GPIO
from config import ROW_PINS, COL_PINS, KEY_MATRIX

class Keyboard:
    def __init__(self, row_pins, col_pins):
        self.row_pins = row_pins
        self.col_pins = col_pins

    def setup(self):
        """Setup the GPIO pins for the keyboard."""
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        # Configure row pins as outputs
        for pin in self.row_pins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.LOW)

        # Configure column pins as inputs with pull-up
        for pin in self.col_pins:
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def get_key(self, key_matrix):
        """Get the pressed key based on the key matrix."""
        for row_pin in self.row_pins:
            GPIO.output(row_pin, GPIO.HIGH)

            for col_pin in self.col_pins:
                if GPIO.input(col_pin) == GPIO.LOW:
                    GPIO.output(row_pin, GPIO.LOW)
                    return key_matrix[self.row_pins.index(row_pin)][self.col_pins.index(col_pin)]

            GPIO.output(row_pin, GPIO.LOW)

        return None

    def cleanup(self):
        """Clean up the GPIO resources."""
        GPIO.cleanup()

def main():
    keyboard = Keyboard(ROW_PINS, COL_PINS)
    keyboard.setup()

    try:
        while True:
            key = keyboard.get_key(KEY_MATRIX)
            if key is not None:
                print("Pressed key:", key)

    except KeyboardInterrupt:
        keyboard.cleanup()

if __name__ == '__main__':
    main()
