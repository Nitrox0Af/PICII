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
    rostos_conhecidos[nome_pessoa] = []
    
    # Percorre todas as imagens na pasta dessa pessoa
    for nome_arquivo in os.listdir(pessoa_pasta):
        imagem = face_recognition.load_image_file(os.path.join(pessoa_pasta, nome_arquivo))
        if len(face_recognition.face_encodings(imagem)) == 0:
            print("Nenhuma face encontrada na imagem {nome_arquivo}")
            continue
        encoding = face_recognition.face_encodings(imagem)[0]
        rostos_conhecidos[nome_pessoa].append(encoding)
        
textfile = open('Encodings/encoding.csv', 'w')
    
for nome, face_encodings in rostos_conhecidos.items():
    textfile.writelines(nome)
    savetxt(f'Encodings/{nome}.csv', face_encodings, delimiter=',')
print("Tap ESC to exit or COMP to take photo")

while True:
    k = input()
    if k == "ESC":
        print("EXIT")
        break
    elif k == "COMP":
        cam = cv2.VideoCapture(0)
        n = 5
        print("Look at the camera")
        print("Taking foto in:")
        while n>0:
            print(n)
            time.sleep(1)
            n-=1
        ret,frame = cam.read()
        if not ret:
            print("failed to grab frame")
            break
        img_name= "data.png"
        cv2.imwrite(img_name,frame)
        cam.release()
    
        # Carrega a imagem desconhecida
        imagem_desconhecida = face_recognition.load_image_file("data.png")
        face_encodings_desconhecido = face_recognition.face_encodings(imagem_desconhecida)
        if len(face_encodings_desconhecido) == 0:
            print("Nenhuma face encontrada na imagem desconhecida")

        # Percorre todas as codificações de rosto na imagem desconhecida
        for face_encoding_desconhecido in face_encodings_desconhecido:
            found_match = False
        
            # Percorre todas as pessoas conhecidas
            for nome, face_encodings in rostos_conhecidos.items():
            
                # Verifica se existe uma correspondência para essa pessoa
                matches = face_recognition.compare_faces(face_encodings, face_encoding_desconhecido)
                if True in matches:
                    found_match = True
                    print(nome)
                    print(f"Esta é a imagem de {nome}")
                    break
        
            # Se não houver correspondência, imprime que a pessoa não é reconhecida
            if not found_match:
                print("Esta pessoa não é reconhecida")
        print("Press ESC to exit or COMP to take photo")
    else:
        print("Invalid command")
        print("Press ESC to exit or COMP to take photo")

