import os
import numpy as np
import face_recognition

# Inicializa a lista de codificações e nomes conhecidos
rostos_conhecidos = {}

# Percorre todas as pastas na pasta 'rostos_conhecidos'
rostos_conhecidos_pasta = "rostos_conhecidos"
for nome_pessoa in os.listdir(rostos_conhecidos_pasta):
    pessoa_pasta = os.path.join(rostos_conhecidos_pasta, nome_pessoa)
    if not os.path.isdir(pessoa_pasta):
        print("aqui")
        continue
    # Inicializa a lista de codificações para essa pessoa
    rostos_conhecidos[nome_pessoa] = []
    
    # Percorre todas as imagens na pasta dessa pessoa
    for nome_arquivo in os.listdir(pessoa_pasta):
        imagem = face_recognition.load_image_file(os.path.join(pessoa_pasta, nome_arquivo))
        if len(face_recognition.face_encodings(imagem)) == 0:
            print(f"Nenhuma face encontrada na imagem {nome_arquivo}")
            continue
        encoding = face_recognition.face_encodings(imagem)[0]
        print(nome_arquivo)
        rostos_conhecidos[nome_pessoa].append(encoding)

# Carrega a imagem desconhecida
imagem_desconhecida = face_recognition.load_image_file("gabi4.jpg")
face_encodings_desconhecido = face_recognition.face_encodings(imagem_desconhecida)
if len(face_encodings_desconhecido) == 0:
    print("Nenhuma face encontrada na imagem desconhecida")
    exit()

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
