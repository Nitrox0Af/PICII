import adafruit_fingerprint
from config import FINGERPRINT_PORT
import serial

print("Inicializando sensor de impressão digital...")
uart = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=1)

print("Criando objeto de sensor de impressão digital...")
finger = adafruit_fingerprint.Adafruit_Fingerprint(uart)

print("Verificando se o sensor está conectado...")
