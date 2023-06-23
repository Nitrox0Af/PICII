import cv2
import RPi.GPIO as GPIO
import time

# Configuração dos pinos do teclado matricial
MATRIX = [
    [1, 2, 3, 'A'],
    [4, 5, 6, 'B'],
    [7, 8, 9, 'C'],
    ['*', 0, '#', 'D']
]

# Pinos GPIO da Raspberry Pi
ROW = [7, 11, 13, 15]
COL = [12, 16, 18, 22]

# Configuração dos pinos GPIO
GPIO.setmode(GPIO.BOARD)

# Configura os pinos da linha como saídas e os pinos da coluna como entradas
for j in range(4):
    GPIO.setup(COL[j], GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(ROW[j], GPIO.OUT)
    GPIO.output(ROW[j], GPIO.HIGH)

def get_key():
    # Varre as linhas do teclado matricial
    for j in range(4):
        GPIO.output(ROW[j], GPIO.LOW)
        
        # Verifica as colunas do teclado matricial
        for i in range(4):
            if GPIO.input(COL[i]) == GPIO.LOW:
                # Retorna o caractere correspondente
                return MATRIX[j][i]

        GPIO.output(ROW[j], GPIO.HIGH)

    return None

def capture_image():
    # Inicializa a webcam
    cap = cv2.VideoCapture(0)

    while True:
        # Lê um quadro da webcam
        ret, frame = cap.read()

        # Mostra o quadro na janela
        cv2.imshow("Webcam", frame)
        key = get_key()
        # Aguarda a tecla 'espaço' para tirar uma foto
        if (cv2.waitKey(1) & 0xFF == ord(' ')) or key == 'A':
            # Salva a imagem capturada
            cv2.imwrite("foto.jpg", frame)
            break

    # Libera a webcam e fecha a janela
    cap.release()
    cv2.destroyAllWindows()

    # Abre a imagem capturada
    img = cv2.imread("foto.jpg")
    cv2.imshow("Foto Capturada", img)
    while True:
        key_main = get_key()
        if (cv2.waitKey(0) & 0xFF == ord(' ')) or key_main == '#':
            cv2.destroyAllWindows()
            GPIO.cleanup()
            break
if __name__ == '__main__':
    capture_image()
