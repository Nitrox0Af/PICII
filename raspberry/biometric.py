import serial
import time
from config import BIOMETRIC_PORT

class Biometric:
    def __init__(self, port):
        self.port = port
        self.serial = None

    def connect(self):
        """Connect to the biometric module."""
        self.serial = serial.Serial(self.port, baudrate=9600, timeout=1)
        time.sleep(2) 

    def enroll_fingerprint(self):
        """Enroll a new fingerprint."""
        print("Coloque o dedo no módulo...")
        while True:
            response = self.serial.readline().strip().decode()
            if response == "OK":
                print("Fingerprint enrolled successfully!")
                break
            elif response == "ERROR":
                print("Error enrolling fingerprint!")
                break

    def verify_fingerprint(self):
        """Verify a fingerprint."""
        print("Coloque o dedo no módulo...")
        while True:
            response = self.serial.readline().strip().decode()
            if response == "MATCH":
                print("Fingerprint verified successfully!")
                break
            elif response == "NO MATCH":
                print("Fingerprint not verified!")
                break

    def disconnect(self):
        """Disconnect from the biometric module."""
        self.serial.close()

def main():
    biometric = Biometric(BIOMETRIC_PORT)
    biometric.connect()

    try:
        biometric.enroll_fingerprint()

        biometric.verify_fingerprint()

    except Exception as e:
        print("An error occurred:", str(e))

    finally:
        biometric.disconnect()

if __name__ == '__main__':
    main()