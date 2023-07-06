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
    
    def test_connection(self):
        """Test the connection with the biometric module."""
        self.serial.write(b"TEST\n")
        response = self.serial.readline().strip().decode()
        if response == "OK":
            print("Connection test successful!")
        else:
            print("Connection test failed!")

def main():
    biometric = Biometric(BIOMETRIC_PORT)  # Insira a porta correta do módulo
    print("Conectando ao módulo...")
    biometric.connect()
    print("Conectado!")

    try:
        print("Testando conexão...")
        biometric.test_connection()
        print("Teste concluído!")

        biometric.enroll_fingerprint()
        print("Impressão digital registrada!")

        # Faça a verificação de impressão digital apenas após a impressão digital ser registrada
        biometric.verify_fingerprint()
        print("Verificação concluída!")

    except Exception as e:
        print("An error occurred:", str(e))

    finally:
        biometric.disconnect()

if __name__ == '__main__':
    main()
