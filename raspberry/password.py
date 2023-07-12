import os
import keyboard
from config import SYSTEM_PASSWORD

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
    
    print("Senha digitada!")
    characters = ""

    if characters == SYSTEM_PASSWORD:
        print("Correct password!")
        print("Abrir Portão!")
    else:
        print("Wrong password!")
        print("Não Abrir!")

if __name__ == "__main__":
    main()
