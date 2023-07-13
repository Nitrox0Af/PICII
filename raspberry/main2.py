import os
import cv2
import threading
import time
import RPi. GPIO as GPIO
import photo_capture
import recognizer
import keyboard
# import reed
from gpiozero import LED, Buzzer, Button
from config import TRIG_PIN, ECHO_PIN, MAX_DISTANCE, MIN_DISTANCE, QNTD_RECOGNIZE, WAITING_TIME, SYSTEM_PASSWORD, RED_LED_PIN, GREEN_LED_PIN, TIME_BLINK, BUZZER_PIN, BUTTON_PIN, DELAY_REED, OPEN_TIME, DEBOUNCE_TIME


# Variável compartilhada
OPEN = False
time_of_change = time.time()


GPIO.setmode(GPIO.BCM)
keyboard.setup()
button = Button(BUTTON_PIN)
led_red = LED(RED_LED_PIN)
# led_green = LED(GREEN_LED_PIN)
buzzer = Buzzer(BUZZER_PIN)
# reed.setup()


def main():
    """Main function."""
    # Criar as threads
    thread_button = threading.Thread(target=button)

    # Iniciar as threads
    thread_button.start()

    while True:
        button.when_pressed = open_gate
        button.when_released = button_released
        display()
        response = keyboard.get_char()
        time.sleep(DEBOUNCE_TIME)
        print("Opção selecionada:	")
        print(response)

        if response == '1':
            os.system('clear')
            print("Iniciando processo de reconhecimento facial...")
            recognizer_face()
        elif response == '2':
            os.system('clear')
            print("\nDigite a senha: ")
            password()
        else:
            print("Opção inválida!")
            time.sleep(DEBOUNCE_TIME)
            continue

    # password()

    # distance_sensor()

    # Criar as threads
    # thread_distance_sensor = threading.Thread(target=distance_sensor)
    # thread_password = threading.Thread(target=password)
    # thread_button = threading.Thread(target=button)
    # thread_close_gate = threading.Thread(target=close_gate)

    # Iniciar as threads
    # thread_distance_sensor.start()
    # thread_password.start()
    # thread_button.start()
    # thread_close_gate.start()

    # Aguardar as threads terminarem
    # thread_distance_sensor.join()
    # thread_password.join()
    # thread_button.join()
    # thread_close_gate.join()


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
    while True:
        have_person = 0
        distance = round(measure_distance())

        if time.time() - time_start > WAITING_TIME*2:
            print("Tempo de espera esgotado!")
            not_open_gate()
            break

        if distance > MAX_DISTANCE:
            print(f"Aproxime-se do sensor.\nA distância máxima é {MAX_DISTANCE}cm. \nDistancia atual: {distance}cm\n\n")
            time.sleep(WAITING_TIME)
            have_person = 0
        elif distance < MIN_DISTANCE:
            print(f"\nAfaste-se do sensor. \nA distância minima é {MIN_DISTANCE}cm. \nDistancia atual: {distance}cm\n\n")
            time.sleep(WAITING_TIME)
        elif distance <= MAX_DISTANCE:
            have_person += 1
            print(f"Pessoa detectada a {distance}cm")
            time.sleep(WAITING_TIME)
            time_start = time.time()
        
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
                        open_gate()
                        break
                else:
                    print("Não Abrir!")
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
        print(char)
        print(characters)
    
    print("Senha digitada!")
    
    if characters == SYSTEM_PASSWORD:
        characters = ""
        print("Correct password!")
        open_gate()
    else:
        characters = ""
        print("Wrong password!")
        not_open_gate()


# def close_gate():
#     """Close gate"""
#     state_reed = reed.get_input()
#     while True:
#         last_state_reed = state_reed
#         state_reed = reed.get_input()

#         if last_state_reed == 1 and state_reed == 0:
#             if (time.time() - time_of_change) >= OPEN_TIME:
#                 # Bloquear o Lock
#                 lock.acquire()
#                 try:
#                     if OPEN:
#                         print("Fechar Portão!")
#                         OPEN = False
#                 finally:
#                     # Liberar o Lock
#                     lock.release()
#                     # blink_led_buzzer(led_green)
#                     blink_led_buzzer(led_red)
#                     display()
                    
#         time.sleep(DELAY_REED)


# def button():
#     """Button"""
#     while True:
#         button.wait_for_press()
#         open_gate()


def open_gate():
    """Open gate"""
    global OPEN, time_of_change
    if not OPEN:
        print("Abrir Portão!")
        time_of_change = time.time()
        OPEN = True
        blink_led(led_red)
        display()

def not_open_gate():
    """Not open gate"""
    print("Não Abrir!")
    blink_led_buzzer(led_red)
    display()

def blink_led_buzzer():
    """Not open gate"""
    print("Não Abrir!")
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


def measure_distance():
    # Envia um pulso curto no pino TRIG
    GPIO.output(TRIG_PIN, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, GPIO.LOW)
    
    # Espera até que o pino ECHO esteja em nível alto
    while GPIO.input(ECHO_PIN) == GPIO.LOW:
        pulse_start = time.time()
    
    # Espera até que o pino ECHO volte para o nível baixo
    while GPIO.input(ECHO_PIN) == GPIO.HIGH:
        pulse_end = time.time()
    
    # Calcula a duração do pulso do ECHO
    pulse_duration = pulse_end - pulse_start
    
    # Calcula a distância com base na velocidade do som (343m/s) e na duração do pulso
    distance = pulse_duration * 34300 / 2
    
    return distance


def button_released():
    """Button released"""
    return None


def button():
    """Button"""
    while True:
        button.wait_for_press()
        open_gate()

main()