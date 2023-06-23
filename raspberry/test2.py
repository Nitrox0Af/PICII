import RPi.GPIO as GPIO
import time

BUTTON_PIN = 20

# Configuração do pino BCM 20 como pull-up interno
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Variáveis para controle do debouncer
button_pressed = False
temp1 = 0.0
temp2 = 0.0

try:
    while True:
        
        # Verifica se o botão foi pressionado
        if GPIO.input(BUTTON_PIN) == GPIO.LOW and not button_pressed:
            button_pressed = True
            temp1 = time.time()  # Armazena o tempo inicial

        # Verifica se o botão foi solto
        while button_pressed:
            temp2 = time.time()  # Armazena o tempo final

            # Verifica o intervalo de tempo
            if temp2 - temp1 > 0.5:
                print("Apertado")
                button_pressed = False
            if GPIO.input(BUTTON_PIN) == GPIO.LOW:
                temp1 = temp2  # Atualiza temp1 para o próximo pressionamento dentro do intervalo

except KeyboardInterrupt:
    print("Programa interrompido pelo usuário")
finally:
    GPIO.cleanup()
