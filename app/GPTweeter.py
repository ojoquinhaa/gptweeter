from tweepy import Client
from openai import ChatCompletion
from threading import Timer
from env import ACCESS_TOKEN, ACCESS_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET, OPENAI_API_KEY
from halo import Halo
from app.Console import clean
from rich import print as rprint


class GPTweeter:
    def __init__(self, subjects: str) -> None:
        self.subjects = subjects  # Definindo os temas

        # Criando o cliente da api do tweeter
        self.client = Client(
            consumer_key=CONSUMER_KEY, consumer_secret=CONSUMER_SECRET,
            access_token=ACCESS_TOKEN, access_token_secret=ACCESS_TOKEN_SECRET
        )

    def activate(self, delay):
        self.tweet()  # Enviando um tweet inicial
        # Publica um tweet de acordo com o delay
        self.set_interval(self.tweet, delay)

    # Função que faz o tweet
    def tweet(self) -> None:
        clean()  # Limpando o console
        response = self.generate_response()  # Gerando o tweeter usando o ChatGPT
        tweet = self.format_tweet(response)  # Formatando o tweet
        self.make_tweet(tweet)  # Fazendo o tweet
        rprint(f"\n[blue]Tweet publicado:[/blue] [yellow]{tweet}[/yellow]")

    # Função que cria um intervalo
    def set_interval(self, func, sec: int):
        # Função que cria o wrapper da função
        def func_wrapper():
            # Criando o intervalo da função com segundos
            self.set_interval(func, sec)
            func()  # Chamando a função passada
        t = Timer(sec, func_wrapper)  # Criando um timer
        t.start()  # Iniciando a Thread
        return t  # Retornando a Thread

    # Função que gera um tweet usando o chat gpt
    def generate_response(self):
        spinner = Halo(text=f'Gerando o tweets sobre {self.subjects} usando o Chat GPT',
                       spinner='dots')  # Gerando o spinner
        spinner.start()  # Iniciando
        try:
            # Gerando a resposta do chat gpt
            response = ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system",
                        "content": f"Você é um robo do tweeter que cria tweets interressante e chamativos falando sobre os assuntos: {self.subjects}"},
                    {"role": "user",
                        "content": "faça um tweet, com no maximo 200 caracteres"},
                ],
                temperature=0.7,
                api_key=OPENAI_API_KEY
            )
        except KeyError:
            spinner.fail(KeyError)  # Caso falhe
        spinner.succeed("Tweet Gerado com sucesso!")  # Sucesso no spinner
        return response  # Retornando a resposta

    # Função que formata o tweeter apartir de uma responsta do chatgpt
    def format_tweet(self, response) -> str:
        spinner = Halo(text='Formatando o tweet',
                       spinner='dots')  # Gerando o spinner
        spinner.start()  # Iniciando o spinner
        # Formatando o texto
        format = response["choices"][0]["message"]["content"]
        spinner.succeed("Tweet formatado com sucesso!")  # Sucesso no spinner
        return format  # Retornando o tweet formatado

    # Função que publica o tweet
    def make_tweet(self, tweet: str):
        spinner = Halo(text='Publicando o tweet',
                       spinner='dots')  # Gerando o spinner
        spinner.start()  # Iniciando o spinner
        try:
            # Fazendo o tweet
            response = self.client.create_tweet(
                text=tweet
            )
        except NameError:
            spinner.fail(NameError)  # Caso falhe
        spinner.succeed("Tweet postado com sucesso!")  # Sucesso no spinner
        return response  # Retornando a resposta
