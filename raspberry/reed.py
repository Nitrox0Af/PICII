import RPi.GPIO as GPIO
from config import REED_SENSOR_PIN

class Reed:
    def __init__(self, pin):
        self.pin = pin
        self.is_triggered = False

    def setup(self):
        """Setup the GPIO pin for the reed sensor."""
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self.pin, GPIO.FALLING, callback=self.triggered, bouncetime=200)

    def triggered(self, channel):
        """Callback function called when the reed sensor is triggered."""
        self.is_triggered = True

    def cleanup(self):
        """Clean up the GPIO resources."""
        GPIO.cleanup()

def main():
    reed_sensor = Reed(REED_SENSOR_PIN)
    reed_sensor.setup()

    try:
        while True:
            if reed_sensor.is_triggered:
                print("Reed sensor triggered!")
                reed_sensor.is_triggered = False

    except KeyboardInterrupt:
        reed_sensor.cleanup()

if __name__ == '__main__':
    main()
