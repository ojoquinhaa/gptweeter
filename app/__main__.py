from cmath import isnan
from app.GPTweeter import GPTweeter

func = input("""
GPTweeter - Bot que usa o Chat GPT para performar tweets chamativos
Qual função você quer utilizar?
1 - Postar um tweet
2 - Postar um tweet de tempo em tempo
""")

subjects = input(
    "Sobre qual temas você quer falar dentro dos seus tweets? (separado por virgula) ")

gptweeter = GPTweeter(subjects)

if (func == "1"):
    gptweeter.tweet()
elif (func == "2"):
    while True:
        delay = input(
            "Qual o intervalo você quer para postar os tweets? (Tempo em segundos maior que 30) ")
        if (delay < 30):
            print("Tempo curto de mais...")
        elif (isnan(delay)):
            print("O delay inserido e invalido...")
        else:
            break
    gptweeter.activate(int(delay))
else:
    print("Função inválida")
