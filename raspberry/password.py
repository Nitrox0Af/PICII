import os
import RPi. GPIO as GPIO
import keyboard
from config import SYSTEM_PASSWORD

GPIO.setmode(GPIO.BCM)
keyboard.setup()

def main():
    """Main function."""
    characters = ""

    while True:
        char = keyboard.get_char()
        if char == "#":
            break
        characters += char

        os.system('clear')
        print("Termine de digitar a senha e pressione # para confirmar.")
        print(char)
    
    print("Senha digitada!")
    print(characters)

    if characters == SYSTEM_PASSWORD:
        characters = ""
        print("Correct password!")
        print("Abrir Portão!")
    else:
        characters = ""
        print("Wrong password!")
        print("Não Abrir!")

if __name__ == "__main__":
    main()
