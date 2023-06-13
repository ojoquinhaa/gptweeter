from tweepy import Client, OAuthHandler
from openai import ChatCompletion
from threading import Timer
from env import ACCESS_TOKEN, ACCESS_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET, OPENAI_API_KEY, BEARER_TOKEN
from halo import Halo
from rich import print as rprint
from requests import get
from time import sleep
from os import system as sys
from platform import system as get_so


class GPTweeter:
    def __init__(self, subjects: str, username: str) -> None:
        # Criando autenticação
        self.auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        self.auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        self.authorization_header = {"Authorization": f"Bearer {BEARER_TOKEN}"}

        # Usuário da conta e temas
        self.username = username
        self.subjects = subjects

        # Criando o cliente da api do tweeter
        self.client = Client(
            consumer_key=CONSUMER_KEY, consumer_secret=CONSUMER_SECRET,
            access_token=ACCESS_TOKEN, access_token_secret=ACCESS_TOKEN_SECRET
        )

    def clean():  # Função para limpar o console
        so = get_so()  # Pegando o sistema operacional
        # Se for windows
        if so == 'windows':
            return sys('cls')  # Função que limpa o console

        # Caso for o resto
        else:
            return sys('clear')  # Função que limpa o console

    def activate(self, delay):
        self.tweet()

        self.set_interval(self.tweet, delay)

        sleep(10)

        self.reply()

        self.set_interval(self.reply, 1800)

    def get_most_recent_reply(self):
        spinner = Halo(text='Fazendo request do tweet mais recente',
                       spinner='dots')  # Gerando o spinner
        spinner.start()  # Iniciando o spinner

        # Parametros para pegar replys
        params = {
            'query': f'to:{self.username} is:reply',
        }

        # Fazendo a request
        request = get('https://api.twitter.com/2/tweets/search/recent',
                      params, headers=self.authorization_header)

        # Formatando request para json
        json = request.json()

        # Retornando erro
        if not json['data']:
            spinner.fail("Falha ao tentar fazer a requisição do último reply")

        spinner.succeed("Reply encontrada com sucesso!")  # Sucesso!

        return json['data'][0]  # Retornando data

    def make_reply(self, tweet: str, reply_id: str):
        spinner = Halo(text='Respondendo último reply',
                       spinner='dots')  # Gerando o spinner
        spinner.start()  # Iniciando o spinner

        try:
            # Respondendo reply
            response = self.client.create_tweet(
                text=tweet,
                in_reply_to_tweet_id=reply_id
            )
        except NameError:
            spinner.fail(NameError)  # Caso falhe

        spinner.succeed("Tweet respondido com sucesso!")  # Sucesso no spinner
        return response  # Retornando a resposta

    def reply(self):
        self.clean()
        last_reply = self.get_most_recent_reply()
        gpt_reply = self.gpt_generate_reply(last_reply['text'])
        formated_reply = self.format_gpt_response(gpt_reply)
        self.make_reply(formated_reply, last_reply['id'])

    def gpt_generate_reply(self, reply: str):
        spinner = Halo(text=f'Gerando a resposta da reply: "{reply}" falando sobre {self.subjects} usando o Chat GPT',
                       spinner='dots')  # Gerando o spinner
        spinner.start()  # Iniciando

        try:
            # Gerando a resposta do chat gpt
            response = ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system",
                        "content": f"Você é um robo do tweeter que cria tweets interressante e chamativos falando sobre os assuntos: {self.subjects}, mas não necessariamente sobre todos os assuntos ao mesmo tempo"},
                    {"role": "user",
                        "content": f'Alguem respondeu o seu tweet com o seguinte reply: "{reply}". Elabore uma resposta.'},
                ],
                temperature=0.7,
                api_key=OPENAI_API_KEY
            )
        except KeyError:
            spinner.fail(KeyError)  # Caso falhe

        spinner.succeed("Reply gerada com sucesso!")  # Sucesso no spinner
        return response  # Retornando a resposta

    # Função que faz o tweet
    def tweet(self) -> None:
        self.clean()  # Limpando o console
        response = self.gpt_generate_tweet()  # Gerando o tweeter usando o ChatGPT
        tweet = self.format_gpt_response(response).replace(
            '"', '')  # Formatando o tweet
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
    def gpt_generate_tweet(self):
        spinner = Halo(text=f'Gerando o tweets sobre {self.subjects} usando o Chat GPT',
                       spinner='dots')  # Gerando o spinner
        spinner.start()  # Iniciando

        try:
            # Gerando a resposta do chat gpt
            response = ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system",
                        "content": f"Você é um robo do tweeter que cria tweets interressante e chamativos falando sobre os assuntos: {self.subjects}, mas não necessariamente sobre todos os assuntos ao mesmo tempo"},
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
    def format_gpt_response(self, response) -> str:
        spinner = Halo(text='Formatando a resposta',
                       spinner='dots')  # Gerando o spinner
        spinner.start()  # Iniciando o spinner
        # Formatando o texto
        format = response["choices"][0]["message"]["content"]
        # Sucesso no spinner
        spinner.succeed("Resposta formatado com sucesso!")
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
