import cv2
import numpy as np
import time

def capture_image():
	# Inicializa a webcam
	cap = cv2.VideoCapture(0)
	while True:
		# Lê um quadro da webcam
		ret, frame = cap.read()
		time.sleep(0.5)
		# Obtém as dimensões da imagem
		height, width, _ = frame.shape

		# Define a mensagem e suas propriedades
		message = "Aperte 1 ou 2"
		font = cv2.FONT_HERSHEY_SIMPLEX
		font_scale = 0.5
		thickness = 1

		# Obtém as dimensões da mensagem
		text_size, _ = cv2.getTextSize(message, font, font_scale, thickness)

		# Define a posição da mensagem
		x = 10
		y = height - text_size[1] - 10

		# Desenha um retângulo preto no fundo
		cv2.rectangle(frame, (x, y), (x + text_size[0], y + text_size[1]), (0, 0, 0), -1)

		# Escreve a mensagem na imagem
		cv2.putText(frame, message, (x, y + text_size[1]), font, font_scale, (255, 255, 255), thickness, cv2.LINE_AA)

		# Mostra o quadro na janela
		cv2.imshow("Webcam", frame)

		# Aguarda a entrada do teclado
		key = cv2.waitKey(1)

		# Captura a foto ao pressionar as teclas 1 ou 2
		if key == ord('1') or key == ord('2'):
			# Salva a imagem capturada
			cv2.imwrite("foto.jpg", frame)
			print("Foto tirada com sucesso!")
			break

	# Libera a webcam e fecha a janela
	cap.release()
	cv2.destroyAllWindows()

	# Abre a imagem capturada
	img = cv2.imread("foto.jpg")

	# Define a mensagem da foto tirada com sucesso
	success_message = "Foto tirada com sucesso"

	# Obtém as dimensões da mensagem
	text_size, _ = cv2.getTextSize(success_message, font, font_scale, thickness)

	# Define a posição da mensagem
	x = (width - text_size[0]) // 2
	y = height - text_size[1] - 10

	# Desenha um retângulo preto no fundo
	cv2.rectangle(img, (x, y), (x + text_size[0], y + text_size[1]), (0, 0, 0), -1)

	# Escreve a mensagem na imagem
	cv2.putText(img, success_message, (x, y + text_size[1]), font, font_scale, (255, 255, 255), thickness, cv2.LINE_AA)

	# Mostra a imagem capturada
	cv2.imshow("Foto Capturada", img)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

# Chama a função para capturar a imagem
capture_image()
