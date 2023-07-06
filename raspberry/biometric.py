import serial
import time

class Biometric:
    def __init__(self, port):
        self.port = port
        self.serial = None

    def connect(self):
        """Connect to the biometric module."""
        self.serial = serial.Serial(self.port, baudrate=9600, timeout=1)
        time.sleep(2)  # Tempo de espera para a inicialização do módulo

    def enroll_fingerprint(self):
        """Enroll a new fingerprint."""
        self.serial.write(b"ENROLL\n")
        response = self.serial.readline().strip().decode()
        if response == "READY":
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
        self.serial.write(b"VERIFY\n")
        response = self.serial.readline().strip().decode()
        if response == "READY":
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
    biometric = Biometric("/dev/ttyUSB0")  # Insira a porta correta do módulo
    biometric.connect()

    try:
        biometric.enroll_fingerprint()

        # Faça a verificação de impressão digital apenas após a impressão digital ser registrada
        biometric.verify_fingerprint()

    except Exception as e:
        print("An error occurred:", str(e))

    finally:
        biometric.disconnect()

if __name__ == '__main__':
    main()