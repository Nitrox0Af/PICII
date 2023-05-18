import subprocess

def run_python_program():
    # Especifica o comando para executar o programa Python
    comando = ['python', 'telegram_bot.py']

    # Executa o comando e captura a saída
    resultado = subprocess.run(comando, capture_output=True, text=True)

    # Verifica se a execução foi bem-sucedida
    if resultado.returncode == 1:
        print("Abrir")
        print("Programa executado com sucesso.")
        print("Saída do programa:")
        print(resultado.stdout)
    elif resultado.returncode == 2:
        print("Fechar")
    else:
        print("Ocorreu um erro durante a execução do programa.")
        print("Erro:")
        print(resultado.stderr)

# Chama a função para executar o programa
run_python_program()
