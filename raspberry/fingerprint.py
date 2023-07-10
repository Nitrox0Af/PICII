import serial
import time
from config import FINGERPRINT_PORT

class Fingerprint:
    def __init__(self, port=FINGERPRINT_PORT, baudrate=9600, timeout=1):
        self.serial = serial.Serial(port, baudrate, timeout=timeout)

    def initialize(self):
        """Inicializa o sensor de impressão digital."""
        self.send_command(0xEF01)
        self.read_response()

    def enroll(self, fingerprint_id):
        """Inicia o processo de cadastro de uma nova impressão digital."""
        self.send_command(0xEF01)
        self.read_response()

        self.send_command(0x01)
        self.read_response()

        self.send_command(fingerprint_id)
        self.read_response()

    def verify(self):
        """Realiza a verificação da impressão digital."""
        self.send_command(0x02)
        response = self.read_response()

        if response == 0x00:
            print("Impressão digital correspondente!")
        else:
            print("Impressão digital não correspondente.")

    def send_command(self, command):
        """Envia um comando para o sensor."""
        self.serial.write(self.int_to_bytes(command))

    def read_response(self):
        """Lê a resposta do sensor."""
        response = self.serial.read(4)
        return self.bytes_to_int(response)

    def int_to_bytes(self, value):
        """Converte um valor inteiro em bytes."""
        return [(value >> (i * 8)) & 0xFF for i in range(3, -1, -1)]

    def bytes_to_int(self, data):
        """Converte um conjunto de bytes em um valor inteiro."""
        return int.from_bytes(data, 'big')

    def close(self):
        """Fecha a conexão com o sensor."""
        self.serial.close()

def main():
    fingerprint_sensor = Fingerprint()

    try:
        fingerprint_sensor.initialize()
        fingerprint_sensor.enroll(1)

        while True:
            fingerprint_sensor.verify()
            time.sleep(1)

    except KeyboardInterrupt:
        fingerprint_sensor.close()

if __name__ == '__main__':
    main()
