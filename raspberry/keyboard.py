import RPi.GPIO as GPIO
from config import ROW_PINS, COL_PINS, KEY_MATRIX

class Keyboard:
    def __init__(self, row_pins, col_pins, key_matrix):
        self.row_pins = row_pins
        self.col_pins = col_pins
        self.key_matrix = key_matrix

    def setup(self):
        """Setup the GPIO pins for the keyboard."""
        GPIO.setmode(GPIO.BCM)
        
        for x in range(0, 4):
            GPIO.setup(self.row_pins[x], GPIO.OUT)
            GPIO.output(self.row_pins[x], GPIO.HIGH)
        
        for x in range(0, 3):
            GPIO.setup(self.col_pins[x], GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def get_key(self):
        """Get the pressed key based on the key matrix."""
        try:
            while True:
                for row_pin in self.row_pins:
                    GPIO.output(row_pin, GPIO.HIGH)
                    result = [GPIO.input(self.col_pins[0]), GPIO.input(self.col_pins[1]), GPIO.input(self.col_pins[2])]
                    
                    if min(result) == 0:
                        key = self.key_matrix[int(self.row_pins.index(row_pin))][int(result.index(0))]
                        GPIO.output(row_pin, GPIO.HIGH)
                        return key
                    GPIO.output(row_pin, GPIO.HIGH)
        except KeyboardInterrupt:
            self.cleanup() 

    def cleanup(self):
        """Clean up the GPIO resources."""
        GPIO.cleanup()

def main():
    keyboard = Keyboard(ROW_PINS, COL_PINS, KEY_MATRIX)
    keyboard.setup()
    keyboard.get_key()

if __name__ == '__main__':
    main()
