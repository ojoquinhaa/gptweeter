from time import sleep
from app.Console import print_header
from datetime import time
from pytz import timezone
from app.GPTweeter import GPTweeter
from schedule import every, run_pending
from time import sleep

config = {
    'USERNAME': 'kevimflores',
    'REPLY_DELAY': 1800,
    'POST_HOURS': [
        time(9, 0, 0),
        time(14, 0, 0),
        time(20, 0, 0)
    ],
    'FUSO': timezone('America/Sao_Paulo'),
    'ASSUNTOS': "Cripto Moeda, Bitcoin, Ether",
}

print_header(config)

gptweeter = GPTweeter(config['ASSUNTOS'], config['USERNAME'])


gptweeter.reply()
gptweeter.activate_replys(config['REPLY_DELAY'])

for post_time in config['POST_HOURS']:
    every().day.at(str(post_time)).do(gptweeter.tweet)

while True:
    run_pending()
    sleep(1)
