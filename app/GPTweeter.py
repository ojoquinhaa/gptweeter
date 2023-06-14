from tweepy import Client, OAuthHandler
from openai import ChatCompletion
from threading import Timer
from env import ACCESS_TOKEN, ACCESS_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET, OPENAI_API_KEY, BEARER_TOKEN
from halo import Halo
from rich import print as rprint
from requests import get
from time import sleep
from app.Console import clean, print_header


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

    def activate(self, delay: int):
        self.tweet()

        self.set_interval(self.tweet, delay)

        sleep(10)

        self.reply()

        self.set_interval(self.reply, 1800)

    def activate_replys(self, delay: int):
        self.set_interval(self.reply, delay)

    def get_most_recent_reply(self):
        spinner = Halo(text='Fazendo request do tweet mais recente',
                       spinner='dots')  # Gerando o spinner
        spinner.start()  # Iniciando o spinner

        # Parametros para pegar replys
        params = {
            'query': f'to:{self.username} is:reply',
            'expansions': 'referenced_tweets.id'
        }

        # Fazendo a request
        request = get('https://api.twitter.com/2/tweets/search/recent',
                      params, headers=self.authorization_header)

        # Formatando request para json
        json = request.json()

        # Retornando erro
        if not 'data' in json:
            spinner.fail("Falha ao tentar fazer a requisição do último reply")
            return None

        spinner.succeed("Reply encontrada com sucesso!")  # Sucesso!

        return json  # Retornando data

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
        clean()

        last_reply = self.get_most_recent_reply()

        if last_reply == None:
            return

        last_reply_data = last_reply['data'][0]
        last_reply_text = last_reply_data['text']
        last_reply_id = last_reply_data['id']

        try:
            last_reply_referenced_tweet = last_reply['includes']['tweets'][0]
            last_reply_referenced_tweet_text = last_reply_referenced_tweet['text']
        except:
            last_reply_referenced_tweet = ""
            last_reply_referenced_tweet_text = ""

        rprint(
            f"[green]Reply:[/green] {last_reply_text} \n[blue]ID:[/blue] {last_reply_id}")

        if self.is_answered(last_reply_id):
            rprint(
                f'[red]A reply - {last_reply_text} - já foi respondida.[/red]')
            return

        gpt_reply = self.gpt_generate_reply(
            reply=last_reply_text,
            referenced_tweet=last_reply_referenced_tweet_text
        )

        formated_reply = self.format_gpt_response(gpt_reply)
        self.make_reply(formated_reply, last_reply_id)

        rprint(
            f"[purple]:Resposta:[/purple] [yellow]{formated_reply}[/yellow]")

    def gpt_generate_reply(self, reply: str, referenced_tweet: str):
        spinner = Halo(text=f'Gerando a resposta da reply: "{reply}" falando sobre {self.subjects} usando o Chat GPT',
                       spinner='dots')  # Gerando o spinner
        spinner.start()  # Iniciando

        try:
            # Gerando a resposta do chat gpt
            response = ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system",
                        "content": f"Você é um robo do tweeter que cria tweets interressante e chamativos para o usuário {self.username} falando sobre os assuntos: {self.subjects}, mas não necessariamente sobre todos os assuntos ao mesmo tempo, é tambem responde replys feitos na conta de forma convidativa, mas sem mencionar nenhum usuário"},
                    {"role": "user",
                        "content": f'Alguem respondeu o seu tweet - {referenced_tweet} - com o seguinte reply: "{reply}". Elabore uma resposta a esté reply, com no maximo 200 caracteres'},
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
        clean()  # Limpando o console
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

    def is_answered(self, id: str):
        with open('app/last_answered_reply.txt', 'r+') as f:
            # Remova quaisquer espaços em branco ou quebras de linha
            last_answered = f.readline().strip()
            if last_answered == id:
                return True
            else:
                f.seek(0)  # Volte para o início do arquivo
                f.truncate()  # Apague todo o conteúdo existente
                f.write(id)  # Escreva o novo ID
                return False
