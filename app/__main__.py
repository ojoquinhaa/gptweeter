from pyfiglet import figlet_format
from rich import print as rprint
from time import sleep
from app.Console import clean
from datetime import time
from pytz import timezone
from app.GPTweeter import GPTweeter
from schedule import every, run_pending
from time import sleep

clean()

title = figlet_format('GPTweeter', font='slant')
rprint(f'[magenta]{title}[/magenta][blue]Uma aplicação python para performar tweets usando o [red]CHAT GPT[/red]![/blue]')
sleep(1)

USERNAME = 'kevimflores'
REPLY_DELAY = 1800
POST_HOURS = [
    time(9, 0, 0),
    time(14, 0, 0),
    time(20, 0, 0)
]
FUSO = timezone('America/Sao_Paulo')
ASSUNTOS = "Cripto Moeda, Bitcoin, Ether"

rprint(
    f"\n[bold]CONFIGURAÇÕES:[/bold] \n[purple]Usuário do Twitter:[/purple] {USERNAME} \n[yellow]Assuntos:[/yellow] {ASSUNTOS}\n[blue]Tempo entre análise de respostas:[/blue] {REPLY_DELAY} \n[red]Horários de postagem definidos: {POST_HOURS[0].hour},{POST_HOURS[1].hour},{POST_HOURS[2].hour}[/red] \n[green]FUSO:[/green]: {FUSO}")

sleep(3)

gptweeter = GPTweeter(ASSUNTOS, USERNAME)

gptweeter.reply()
gptweeter.activate_replys(1800)

for post_time in POST_HOURS:
    every().day.at(str(post_time)).do(gptweeter.tweet)

while True:
    run_pending()
    sleep(1)
