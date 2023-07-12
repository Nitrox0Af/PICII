import os
import time
import photo_capture
import recognizer
import keyboard
import RPi. GPIO as GPIO
from gpiozero import DistanceSensor
from config import MAX_DISTANCE, MIN_DISTANCE, QNTD_RECOGNIZE, WAITING_TIME, ECHO_PIN, TRIG_PIN

GPIO.setmode(GPIO.BCM)
ultrasonic = DistanceSensor(echo=ECHO_PIN, trigger=TRIG_PIN)
keyboard.setup()

def main():
    """Main function."""
    have_person = 0
    while True:
        distance = ultrasonic.distance * 100

        if distance > MAX_DISTANCE:
            time.sleep(1)
        elif distance <= MAX_DISTANCE:
            have_person += 1
            print(f"Pessoa detectada a {distance}cm")
            time.sleep(WAITING_TIME)
        elif distance < MIN_DISTANCE:
            print(f"Afaste-se do sensor. A distância minima é {MIN_DISTANCE}cm. Distancia atual: {distance}cm")
            time.sleep(WAITING_TIME)
        
        if have_person >= QNTD_RECOGNIZE:
            os.system('clear')
            have_person = 0

            print("Iniciando processo de tirar foto...")
            take_photo = photo_capture.main()

            if take_photo:
                print("Iniciando processo de reconhecimento...")
                open_gate = recognizer.main()
                if open_gate:
                    print("Abrir Portão!")
                else:
                    print("Não Abrir!")

if __name__ == "__main__":
    main()
