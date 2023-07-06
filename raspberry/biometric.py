from pyfingerprint import PyFingerprint

# Inicialização do leitor de impressões digitais
try:
    fingerprint = PyFingerprint('/dev/ttyAMA0', 57600, 0xFFFFFFFF, 0x00000000)
    if not fingerprint.verifyPassword():
        raise ValueError('Senha incorreta')

except Exception as e:
    print(f'Erro ao inicializar o leitor de impressões digitais: {e}')
    exit(1)

# Verificação de uma impressão digital
try:
    print('Coloque o dedo no leitor...')
    while not fingerprint.readImage():
        pass

    fingerprint.convertImage(0x01)
    result = fingerprint.searchTemplate()
    position = result[0]

    if position >= 0:
        print(f'Impressão digital encontrada na posição #{position}')
    else:
        print('Impressão digital não encontrada')

except Exception as e:
    print(f'Erro na verificação da impressão digital: {e}')
    exit(1)

# Limpeza
fingerprint.close()
