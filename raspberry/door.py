import time
from relay import Relay
from reed_sensor import ReedSensor
from config import REED_SENSOR_PIN, RELAY_PIN

class Door:
    def __init__(self, reed_pin, relay_pin):
        self.reed_sensor = ReedSensor(reed_pin)
        self.relay = Relay(relay_pin)
        self.is_open = False

    def setup(self):
        """Setup the door controller."""
        self.reed_sensor.setup()
        self.relay.setup()

    def control_door(self):
        """Control the door based on sensor and relay states."""
        try:
            while True:
                if self.relay.is_on:
                    # Relay is activated, open the door
                    if not self.is_open:
                        self.is_open = True
                        print("Opening the door...")
                        self.relay.turn_on()

                if self.reed_sensor.is_triggered and not self.relay.is_on:
                    # Reed sensor detected a magnetic field, close the door
                    if self.is_open:
                        self.is_open = False
                        print("Closing the door...")
                        self.relay.turn_off()

                time.sleep(0.1)

        except KeyboardInterrupt:
            self.cleanup()

    def cleanup(self):
        """Clean up the resources."""
        self.reed_sensor.cleanup()
        self.relay.cleanup()

    def main(self):
        self.setup()
        self.control_door()

if __name__ == '__main__':
    door = Door(REED_SENSOR_PIN, RELAY_PIN)
    door.main()
