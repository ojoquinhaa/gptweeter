from app.GPTweeter import GPTweeter
from app.Console import Colors, clean
from time import sleep
from pyfiglet import figlet_format
from rich import print as rprint

colors = Colors()  # Classe das cores
clean()  # Limpando o console

# Apresentação
title = figlet_format('GPTweeter', font='slant')
rprint(f'[magenta]{title}[/magenta][blue]Uma aplicação python para performar tweets usando o [red]CHAT GPT[/red]![/blue]')

sleep(1)  # Espera um segundo

# Pergunta inicial para escolher qual função o programa irá performar
func = input(f"""{colors.BOLD}Qual função você quer utilizar?

{colors.OKCYAN}1 - Postar um tweet
2 - Postar um tweet de tempo em tempo
3 - Responda um reply

{colors.HEADER}Função: {colors.WARNING}""")

clean()  # Limpando o console

# Segunda pergunta que vai definir os temas dos tweets
subjects = input(
    f"{colors.UNDERLINE}Sobre qual temas você quer falar dentro dos seus tweets? (separado por virgula) {colors.OKGREEN}")

clean()  # Limpando o console

# Terceira pergunta que vai definir o nome de usuário da conta
username = input(
    f"{colors.HEADER}Qual o nome de usuário da conta autenticada? (sem o @) {colors.FAIL}"
)

gptweeter = GPTweeter(subjects, username)  # Criando a instancia com os temas

# Caso a função escolhida seja a primeira
if (func == "1"):
    gptweeter.tweet()  # Performe um tweet

# Caso a função escolhida seja a segunda
elif (func == "2"):
    while True:  # Cria um loop
        # Pergunta o tempo de delay de um tweet para o outro
        delay = input(
            f"{colors.UNDERLINE}Qual o intervalo você quer para postar os tweets? (Tempo, em segundos, maior que 60) {colors.OKBLUE}")

        # Caso o tempo não seja um numero
        if (not delay.strip().isdigit()):
            # Retornando erro e repetindo a pergunta
            print("O delay inserido e invalido...")
            sleep(1)  # aguardando um segundo
            clean()  # Limpando o console

        # Caso o tempo seja menor que 1 minuto (para evitar bugs)
        elif (int(delay) < 60):
            # Retornando o erro e repetindo a pergunta
            print("Tempo curto de mais...")
            sleep(1)  # aguardando um segundo
            clean()  # Limpando o console

        # Caso esteja tudo certo
        else:
            break  # Quebra o loop

    clean()  # Limpando o console

    # Iniciando o thread do gptweeter
    gptweeter.activate(int(delay))

elif (func == "3"):
    gptweeter.reply()

# Caso não seja nenhuma das funções
else:
    print("Função inválida")  # Retornando erro
