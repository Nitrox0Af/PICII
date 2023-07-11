import adafruit_fingerprint
from config import FINGERPRINT_PORT
import serial
uart = serial.Serial(FINGERPRINT_PORT, baudrate=57600, timeout=1)

finger = adafruit_fingerprint.Adafruit_Fingerprint(uart)
