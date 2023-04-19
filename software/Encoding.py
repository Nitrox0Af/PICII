import os
import numpy as np
import face_recognition
import cv2
import time
from numpy import asarray
from numpy import savetxt

# Inicializa a lista de codificações e nomes conhecidos
rostos_conhecidos = {}
print("Initializing encoding of database photos, please wait...")
# Percorre todas as pastas na pasta 'rostos_conhecidos'
rostos_conhecidos_pasta = "rostos_conhecidos"
for nome_pessoa in os.listdir(rostos_conhecidos_pasta):
    pessoa_pasta = os.path.join(rostos_conhecidos_pasta, nome_pessoa)
    if not os.path.isdir(pessoa_pasta):
        continue
    # Inicializa a lista de codificações para essa pessoa
    print(nome_pessoa)
    rostos_conhecidos[nome_pessoa] = []
    
    # Percorre todas as imagens na pasta dessa pessoa
    for nome_arquivo in os.listdir(pessoa_pasta):
        imagem = face_recognition.load_image_file(os.path.join(pessoa_pasta, nome_arquivo))
        if len(face_recognition.face_encodings(imagem)) == 0:
            print("Nenhuma face encontrada na imagem {nome_arquivo}")
            continue
        encoding = face_recognition.face_encodings(imagem)[0]
        print(type(encoding))
        rostos_conhecidos[nome_pessoa].append(encoding)
        
textfile = open('Encodings/encoding.txt', 'w')
flag=0
for nome, face_encodings in rostos_conhecidos.items():
		if flag != 0: 
			aux=','+nome
		elif flag == 0: 
			aux = nome
			flag+=1
		textfile.writelines(aux)
		savetxt(f'Encodings/{nome}.txt', face_encodings, delimiter=',')
print("DONE!")
