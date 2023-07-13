import os
import cv2
import time
import RPi. GPIO as GPIO
import photo_capture
import recognizer
import keyboard
import reed
from gpiozero import DistanceSensor, LED, Buzzer, Button
from config import TRIG_PIN, ECHO_PIN, MAX_DISTANCE, MIN_DISTANCE, QNTD_RECOGNIZE, WAITING_TIME, SYSTEM_PASSWORD, RED_LED_PIN, GREEN_LED_PIN, TIME_BLINK, BUZZER_PIN, BUTTON_PIN, DELAY_REED, OPEN_TIME, DEBOUNCE_TIME


OPEN = False
time_of_change = time.time()


GPIO.setmode(GPIO.BCM)
ultrasonic = DistanceSensor(echo=ECHO_PIN, trigger=TRIG_PIN)
keyboard.setup()
button = Button(BUTTON_PIN)
led_red = LED(RED_LED_PIN)
# led_green = LED(GREEN_LED_PIN)
buzzer = Buzzer(BUZZER_PIN)
reed.setup()


def main():
    """Main function."""
    button.when_pressed = open_gate

    while True:
        display()
        response = keyboard.get_char()
        time.sleep(DEBOUNCE_TIME)
        print("Opção selecionada:	", response)

        if response == '1':
            os.system('clear')
            print("\nIniciando processo de reconhecimento facial...")
            recognizer_face()
        elif response == '2':
            os.system('clear')
            print("\nDigite a senha: ")
            password()
        else:
            print("\nOpção inválida!")
            time.sleep(DEBOUNCE_TIME)
            continue


def display():
    """Displays"""
    os.system('clear')
    print("\n")
    print("\n")
    print("Digite uma opção para entrar na residência: ")
    print("\n")
    print("1 - Entrar com Reconhecimento Facial")
    print("\n")
    print("2 - Entrar com Senha")
    print("\n")
    print("\n")


def recognizer_face():
    time_start = time.time()
    have_person = 0
    while True:
        distance = round(ultrasonic.distance * 100)

        if time.time() - time_start > WAITING_TIME*2:
            print("\nTempo de espera esgotado!")
            not_open_gate()
            break

        if distance > MAX_DISTANCE:
            print(f"\nAproxime-se do sensor.\nA distância máxima é {MAX_DISTANCE}cm. \nDistancia atual: {distance}cm\n\n")
            time.sleep(WAITING_TIME)
            have_person = 0
        elif distance < MIN_DISTANCE:
            print(f"\nAfaste-se do sensor. \nA distância minima é {MIN_DISTANCE}cm. \nDistancia atual: {distance}cm\n\n")
            time.sleep(WAITING_TIME)
        elif distance <= MAX_DISTANCE:
            have_person += 1
            print(f"\nPerfeito! Você detectado(a) a {distance}cm")
            time.sleep(WAITING_TIME)
            time_start = time.time()
        
        if have_person >= QNTD_RECOGNIZE:
            os.system('clear')
            have_person = 0

            print("\nIniciando processo de tirar foto...")
            take_photo = photo_capture.main()
            
            if take_photo:
                print("\nIniciando processo de reconhecimento...")
                open_gate = recognizer.main()
                if open_gate:
                        print("\nAbrir Portão!")
                        open_gate()
                        break
                else:
                    print("\nNão Abrir!")
                    not_open_gate()
                    break


def password():
    characters = ""

    while True:
        char = keyboard.get_char()
        time.sleep(DEBOUNCE_TIME)
        if char == "#":
            break
        characters += char

        os.system('clear')
        print("\nTermine de digitar a senha e pressione # para confirmar.")
    
    print("\nSenha digitada!")
    
    if characters == SYSTEM_PASSWORD:
        characters = ""
        print("Correct password!")
        open_gate()
    else:
        characters = ""
        print("Wrong password!")
        not_open_gate()


def close_gate():
    """Close gate"""
    time_of_change = time.time()
    while True:
        if not reed.get_input():
            if (time.time() - time_of_change) >= OPEN_TIME:
                print("\nFechar Portão!")
                blink_led(led_red)
                    
        time.sleep(DELAY_REED)


def open_gate():
    """Open gate"""
    if reed.get_input():
        print("\nAbrir Portão!")
        blink_led_buzzer(led_red)
        close_gate()
        display()
    else:
        print("\nPortão já está aberto!")


def not_open_gate():
    """Not open gate"""
    print("\nNão Abrir!")
    blink_led(led_red)
    display()


def blink_led(led):
    """Blink led"""
    time_start = time.time()
    while (time.time() - time_start) < TIME_BLINK:
        led.blink()
    led.off()


def blink_led_buzzer(led):
    """Blink led"""
    time_start = time.time()
    while (time.time() - time_start) < TIME_BLINK:
        led.blink()
        buzzer.beep()
    led.off()
    buzzer.off()


try:
    main()
except KeyboardInterrupt:
    GPIO.cleanup()