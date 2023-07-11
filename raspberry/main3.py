import os
from gpiozero import DistanceSensor
from config import TRIG_PIN, ECHO_PIN, MAX_DISTANCE, MIN_DISTANCE, ROW_PINS, COL_PINS, KEY_MATRIX
from keyboard import Keyboard
from photo_capture import main

def main():
    """Main function."""
    ultrasonic = DistanceSensor(echo=ECHO_PIN, trigger=TRIG_PIN)

    keyboard = Keyboard(ROW_PINS, COL_PINS, KEY_MATRIX)
    keyboard.setup()

    while True:
        choice = display_menu(keyboard)

        if choice == "1":
            facial_recognition(ultrasonic, keyboard)

        elif choice == "2":
            process_password_choice(keyboard)

        else:
            print("Opção inválida!")
            continue
        break


def display_menu(keyboard):
    """Displays the menu and obtains user's choice."""
    os.system('clear')
    print("Escolha uma opção: ")
    print("1 - Reconhecimento Facial")
    print("2 - Senha")

    key = keyboard.get_key()
    print("Opção escolhida:", key)
    return key


def facial_recognition(ultrasonic):
    """Performs facial recognition."""
    if ultrasonic.distance <= MAX_DISTANCE:
        if ultrasonic.distance >= MIN_DISTANCE:
            print("Iniciando o Reconhecimento Facial...")
            photo_capture.main(keyboard)
        else:
            print("Aproxime-se da camera! Sua distância é de", ultrasonic.distance*100, "cm.")
    else:
        print("Afastem-se da camera! Sua distância é de", ultrasonic.distance*100, "cm.")


def display_password(keyboard):
    """Performs password."""
    os.system('clear')
    print("Escolha uma opção: ")
    print("1 - Entrar com a senha")
    print("2 - Alterar a senha")
    print("0 - Voltar")

    key = keyboard.get_key()
    print("Opção escolhida:", key)
    return key


def process_password_choice(keyboard):
    """Process password Choice."""
    while True:
        choice = display_password(keyboard)
        if choice == "1":
            print("Digite a senha: ")
        elif choice == "2":
            print("Digite a senha segura: ")
        elif choice == "0":
            return
        else:
            print("Opção inválida!")
            continue


main()