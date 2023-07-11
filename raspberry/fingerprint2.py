import adafruit_fingerprint
from config import FINGERPRINT_PORT
import serial

uart = serial.Serial("/dev/ttyS0", baudrate=57600, timeout=1)

print("OK")
finger = adafruit_fingerprint.Adafruit_Fingerprint(uart)
print("Waiting for fingerprint ...")
