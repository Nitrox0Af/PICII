import cv2

def capture_image():
    # Inicializa a webcam
    cap = cv2.VideoCapture(0)

    while True:
        # Lê um quadro da webcam
        ret, frame = cap.read()

        # Mostra o quadro na janela
        cv2.imshow("Webcam", frame)

        # Aguarda a tecla 'espaço' para tirar uma foto
        if cv2.waitKey(1) & 0xFF == ord(' '):
            # Salva a imagem capturada
            cv2.imwrite("foto.jpg", frame)
            break

    # Libera a webcam e fecha a janela
    cap.release()
    cv2.destroyAllWindows()

    # Abre a imagem capturada
    img = cv2.imread("foto.jpg")
    cv2.imshow("Foto Capturada", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    capture_image()

