import adafruit_fingerprint
from config import FINGERPRINT_PORT
import serial

vai = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=1)

print("OK")
finger = adafruit_fingerprint.Adafruit_Fingerprint(vai)
print("Waiting for fingerprint ...")
