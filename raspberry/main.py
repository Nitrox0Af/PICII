import RPi.GPIO as GPIO
import time
import cv2

import recognizer
import config

# Configuração teclado matricial 4x4
# R - Linha; C - Colunas
R1 = 7
R2 = 11
R3 = 13
R4 = 15

C1 = 12
C2 = 16
C3 = 18
C4 = 22

# Flag
LOCKED = 1

# Configuração dos LEDs
RED_LED_PIN = 10
GREEN_LED_PIN = 8

# Configuração do botão
BUTTON_PIN = 38

# Configuração do sensor de distância
# Define os pinos TRIG e ECHO
TRIG_PIN = 32
ECHO_PIN = 36

PASSWORD = ""
SYSTEM_PASSWORD = "1234"
button_pressed = False
temp1 = 0.0
temp2 = 0.0
keyBoard=[["1", "2", "3", "A"],
		  ["4", "5", "6", "B"],
		  ["7", "8", "9", "C"],
		  ["*", "0", "#", "D"]]
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

GPIO.setup(R1, GPIO.OUT)
GPIO.setup(R2, GPIO.OUT)
GPIO.setup(R3, GPIO.OUT)
GPIO.setup(R4, GPIO.OUT)

GPIO.setup(C1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.setup(GREEN_LED_PIN, GPIO.OUT)
GPIO.setup(RED_LED_PIN, GPIO.OUT)

GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)

def main():
	have_person = 0
	while True:
		dist = round(measure_distance())
		if dist > config.MAX_DISTANCE:
			print(f"Aproxime no max 40cm. Distancia atual: {dist}cm")
			have_person = 0
		elif config.MAX_DISTANCE <= 40:
			have_person += 1
			print(f"Pessoa detectada a {dist}cm")
		# if dist < 5:
		# 	print("Afaste-se do sensor")
		# 	have_person += 1
		if have_person >= config.QNTD_RECOGNIZE:
			print("Iniciando processo de reconhecimento...")
			capture_an_image()
		time.sleep(config.TIME_TO_RECOGNIZE)

def capture_an_image():
	"""Capture an image from the camera"""
	time_start = time.time()
	time_end = time.time()
	cap = cv2.VideoCapture(0)
	flag = 0
	while True:
		# Lê um quadro da webcam
		ret, frame = cap.read()
		if frame is None:
            # Lidar com a falta de um quadro válido da webcam
            # Exibir uma mensagem de erro, tentar novamente ou sair do loop
			print("Erro ao capturar imagem!")
			time.sleep(1)
			continue
		time_end = time.time()
		# Obtém as dimensões da imagem
		height, width, _ = frame.shape

		# Desenha a mensagem na imagem
		message = f"Prepare-se para a foto vai ser tirada em {config.TIME_TO_TAKE_PHOTO} segundos!"
		font = cv2.FONT_HERSHEY_SIMPLEX
		font_scale = 0.5
		thickness = 1
		
		font = cv2.FONT_HERSHEY_SIMPLEX
		font_scale = 0.5
		thickness = 1

		# Obtém as dimensões da mensagem
		text_size, _ = cv2.getTextSize(message, font, font_scale, thickness)
		# Define a posição da mensagem
		x = 10
		y = height - text_size[1] - 10

		# Desenha um retângulo preto no fundo
		cv2.rectangle(frame, (x-4, y-4), (x + text_size[0]+4, y + text_size[1]+4), (0, 0, 0), -1)

		# Escreve a mensagem na imagem
		cv2.putText(frame, message, (x, y + text_size[1]), font, font_scale, (255, 255, 255), thickness, cv2.LINE_AA)
		# Mostra o quadro na janela
		cv2.imshow("Webcam", frame)

		# Captura a foto ao pressionar as teclas 1 ou 2
		if (time_end - time_start) >= config.TIME_TO_TAKE_PHOTO:
			# Salva a imagem capturada
			cv2.imwrite(config.POTHO_PATH, frame)
			cap.release()
			cv2.destroyAllWindows()
			time.sleep(1)

			
			img = cv2.imread(config.POTHO_PATH)
			message = "Precione #, se preferir tirar outra foto"
			font = cv2.FONT_HERSHEY_SIMPLEX
			font_scale = 0.5
			thickness = 1

			# Obtém as dimensões da mensagem
			text_size, _ = cv2.getTextSize(message, font, font_scale, thickness)
			# Define a posição da mensagem
			x = 10
			y = height - text_size[1] - 10

			# Desenha um retângulo preto no fundo
			cv2.rectangle(img, (x-4, y-4), (x + text_size[0]+4, y + text_size[1]+4), (0, 0, 0), -1)

			# Escreve a mensagem na imagem
			cv2.putText(img, message, (x, y + text_size[1]), font, font_scale, (255, 255, 255), thickness, cv2.LINE_AA)
			cv2.imshow("Foto Capturada", img)

def check_distance(dist):
	"""Check if the distance is between the max and min distance"""
	have_person = 0
	if dist > config.MAX_DISTANCE:
		print(f"Aproxime no max 40cm. Distancia atual: {dist}cm")
		have_person = 0
	elif config.MAX_DISTANCE <= 40:
		have_person += 1
		print("Pessoa detectada")
	# if dist < 5:
	# 	print("Afaste-se do sensor")
	# 	have_person += 1
	if have_person >= config.QNTD_RECOGNIZE:
		return True
	time.sleep(config.TIME_TO_RECOGNIZE)

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

def get_char(row, char):
	GPIO.output(row, GPIO.HIGH)
	if GPIO.input(C1) == 1:
		GPIO.output(row, GPIO.LOW)
		return char[0]
	if GPIO.input(C2) == 1:
		GPIO.output(row, GPIO.LOW)
		return char[1]
	if GPIO.input(C3) == 1:
		GPIO.output(row, GPIO.LOW)
		return char[2]
	if GPIO.input(C4) == 1:
		GPIO.output(row, GPIO.LOW)
		return char[3]
	GPIO.output(row, GPIO.LOW)
	return "P"

def take_picture():
	time_start = time.time()
	time_end = time.time()
	cap = cv2.VideoCapture(0)
	flag = 0
	while True:
		# Lê um quadro da webcam
		ret, frame = cap.read()
		if frame is None:
            # Lidar com a falta de um quadro válido da webcam
            # Exibir uma mensagem de erro, tentar novamente ou sair do loop
			print("Erro ao capturar imagem!")
			time.sleep(1)
			continue
		time_end = time.time()
		# Obtém as dimensões da imagem
		height, width, _ = frame.shape

		# Desenha a mensagem na imagem
		message = f"Prepare-se para a foto vai ser tirada em {config.TIME_TO_TAKE_PHOTO} segundos!"
		font = cv2.FONT_HERSHEY_SIMPLEX
		font_scale = 0.5
		thickness = 1
		
		font = cv2.FONT_HERSHEY_SIMPLEX
		font_scale = 0.5
		thickness = 1

		# Obtém as dimensões da mensagem
		text_size, _ = cv2.getTextSize(message, font, font_scale, thickness)
		# Define a posição da mensagem
		x = 10
		y = height - text_size[1] - 10

		# Desenha um retângulo preto no fundo
		cv2.rectangle(frame, (x-4, y-4), (x + text_size[0]+4, y + text_size[1]+4), (0, 0, 0), -1)

		# Escreve a mensagem na imagem
		cv2.putText(frame, message, (x, y + text_size[1]), font, font_scale, (255, 255, 255), thickness, cv2.LINE_AA)
		# Mostra o quadro na janela
		cv2.imshow("Webcam", frame)

		# Captura a foto ao pressionar as teclas 1 ou 2
		if (time_end - time_start) >= config.TIME_TO_TAKE_PHOTO:
			# Salva a imagem capturada
			cv2.imwrite(config.POTHO_PATH, frame)
			cap.release()
			cv2.destroyAllWindows()
			time.sleep(1)

			
			img = cv2.imread(config.POTHO_PATH)
			message = "Precione #, se preferir tirar outra foto"
			font = cv2.FONT_HERSHEY_SIMPLEX
			font_scale = 0.5
			thickness = 1

			# Obtém as dimensões da mensagem
			text_size, _ = cv2.getTextSize(message, font, font_scale, thickness)
			# Define a posição da mensagem
			x = 10
			y = height - text_size[1] - 10

			# Desenha um retângulo preto no fundo
			cv2.rectangle(img, (x-4, y-4), (x + text_size[0]+4, y + text_size[1]+4), (0, 0, 0), -1)

			# Escreve a mensagem na imagem
			cv2.putText(img, message, (x, y + text_size[1]), font, font_scale, (255, 255, 255), thickness, cv2.LINE_AA)
			cv2.imshow("Foto Capturada", img)
			while True:
				key = cv2.waitKey(1)
				key2=get_char(R1, ["1", "2", "3", "A"])
				# Captura a foto ao pressionar as teclas 1 ou 2
				if key == ord('2') or key2 == "A":
					cv2.destroyAllWindows()
					flag = 0
					break
				key2=get_char(R2, ["4", "5", "6", "B"])
				if key == ord('1') or key == ord('2') or key2 == "B":
					cv2.destroyAllWindows()
					flag = 1
					break
			if flag == 0:
				open_gate = recognizer.main()
				time.sleep(0.5)
				control_gate(open_gate)
				break
			else:
				time.sleep(0.5)
				cap = cv2.VideoCapture(0)
				continue

def control_gate(open_gate: bool) -> None:
	if open_gate:
		# Pisca o LED verde 3 vezes
		for _ in range(3):
			GPIO.output(GREEN_LED_PIN, GPIO.HIGH)
			time.sleep(1)
			GPIO.output(GREEN_LED_PIN, GPIO.LOW)
			time.sleep(0.5)
		print("Destrancado")
		PASSWORD = ""
		LOCKED = 0
	else:
		for _ in range(3):
			GPIO.output(RED_LED_PIN, GPIO.HIGH)
			time.sleep(1)
			GPIO.output(RED_LED_PIN, GPIO.LOW)
			time.sleep(0.5)

def printChar(row, char):
	global PASSWORD, LOCKED
	GPIO.output(row, GPIO.HIGH)
    
	if LOCKED == 1:
		if GPIO.input(C1) == 1:
			PASSWORD += char[0]
			time.sleep(0.1)
		if GPIO.input(C2) == 1:
			PASSWORD += char[1]
			time.sleep(0.1)
		if GPIO.input(C3) == 1:
			if char[2] == "#":
				print(PASSWORD)
				if PASSWORD == SYSTEM_PASSWORD:
					# Pisca o LED verde 3 vezes
					for _ in range(3):
						GPIO.output(GREEN_LED_PIN, GPIO.HIGH)
						time.sleep(1)
						GPIO.output(GREEN_LED_PIN, GPIO.LOW)
						time.sleep(0.5)
					print("Destrancado")
					PASSWORD = ""
					LOCKED = 0
				else:
					for _ in range(3):
						GPIO.output(RED_LED_PIN, GPIO.HIGH)
						time.sleep(1)
						GPIO.output(RED_LED_PIN, GPIO.LOW)
						time.sleep(0.5)
					print("Senha errada")
					PASSWORD = ""
			else:
				PASSWORD += char[2]
				time.sleep(0.1)
		if GPIO.input(C4) == 1:
			if char[3] == "A":
				take_picture()
				PASSOWORD = ""
			else:
				PASSWORD += char[3]
				time.sleep(0.1)
	else:
		if GPIO.input(C1) == 1 or GPIO.input(C2) == 1 or GPIO.input(C3) == 1:
			print("Porta está aberta")
			time.sleep(0.1)
		if GPIO.input(C4) == 1:
			if char[3] == "D":
				print("Porta trancada")
				LOCKED = 1
				time.sleep(0.1)
			else:
				print("Porta está aberta")
				time.sleep(0.1)
	GPIO.output(row, GPIO.LOW)

# try:
#     while True:
#         # Verifica se o botão foi pressionado
#         while GPIO.input(BUTTON_PIN) == GPIO.LOW and not button_pressed:
#             button_pressed = True
#             temp1 = time.time()  # Armazena o tempo inicial

#         # Verifica se o botão foi solto
#         while button_pressed:
#             temp2 = time.time()  # Armazena o tempo final

#             # Verifica o intervalo de tempo
#             if temp2 - temp1 > 0.5:
#                 if LOCKED == 1:
#                     print("Destrancado")
#                     LOCKED = 0
#                 else:
#                     print("Porta está aberta")
#                 button_pressed = False

#             if GPIO.input(BUTTON_PIN) == GPIO.LOW:
#                 temp1 = temp2  # Atualiza temp1 para o próximo pressionamento dentro do intervalo

#         printChar(R1, ["1", "2", "3", "A"])
#         printChar(R2, ["4", "5", "6", "B"])
#         printChar(R3, ["7", "8", "9", "C"])
#         printChar(R4, ["*", "0", "#", "D"])
        
#         #if PASSWORD.endswith("A"):
#             # Acionar o sensor de distância
#             # Verificar se objeto está a menos de 20 cm do sensor
#             # Se estiver, capturar a foto e exibir ao usuário
#             #PASSWORD = ""
#             #capture_photo()
            
        
#         time.sleep(0.1)

# except KeyboardInterrupt:
#     print("Stopped")

main()