from os import system as sys
from platform import system as get_so


def clean():  # Função para limpar o console
    so = get_so()  # Pegando o sistema operacional
    # Se for windows
    if so == 'windows':
        return sys('cls')  # Função que limpa o console

    # Caso for o resto
    else:
        return sys('clear')  # Função que limpa o console


class Colors:  # Classe das cores
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
