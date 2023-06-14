from os import system as sys
from platform import system as get_so
from pyfiglet import figlet_format
from rich import print as rprint
from time import sleep


def clean():  # Função para limpar o console
    so = get_so()  # Pegando o sistema operacional
    # Se for windows
    if so == 'windows':
        return sys('cls')  # Função que limpa o console

    # Caso for o resto
    else:
        return sys('clear')  # Função que limpa o console


def print_header(config):
    title = figlet_format('GPTweeter', font='slant')
    rprint(
        f'[magenta]{title}[/magenta][blue]Uma aplicação python para performar tweets usando o [red]CHAT GPT[/red]![/blue]')
    sleep(1)
    rprint(f"""
[bold]CONFIGURAÇÕES:[/bold]
[purple]Usuário do Twitter:[/purple] {config['USERNAME']}
[yellow]Assuntos:[/yellow] {config['ASSUNTOS']}
[blue]Tempo entre análise de respostas:[/blue] {config['REPLY_DELAY']}
[red]Horários de postagem definidos:[/red] {config['POST_HOURS'][0].hour},{config['POST_HOURS'][1].hour},{config['POST_HOURS'][2].hour}
[green]FUSO:[/green]: {config['FUSO']}""")
    sleep(3)


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
