# GPTweeter

Uma aplicação python que cria tweets utilizando a API do [Chat GPT](https://platform.openai.com/docs/guides/chat/introduction) e então postam eles em alguma conta usando o [Tweepy](https://www.tweepy.org/)

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)

## Uso/Exemplos

Primeiro clone o repositorio usando o [git](https://git-scm.com/)

```bash
git clone https://github.com/ojoquinhaa/gptweeter.git gptweeter
cd gptweeter
```

Após isso crie uma env dentro da sua pasta usando o comando

```bash
python3 -m venv venv
```

Acesse seu env

```bash
windows:
> venv/Scripts/activate
linux/mac:
& source ./venv/bin/activate
```

Então, faça o dowload de todas as dependencias do projeto usando o [pip](https://pypi.org/project/pip/), dentro do seu env

```bash
pip3 install -r requirements.txt
```

Crie um arquivo `.env` na pasta raiz do projeto então adicione as seguintes variaveis de ambiente

```bash
OPENAI_API_KEY=chave_da_api_openai
CONSUMER_KEY=chave_de_consumidor_do_twitter
CONSUMER_SECRET=segredo_de_consumidor_do_twitter
ACCESS_TOKEN=token_de_acesso_do_twitter
ACCESS_TOKEN_SECRET=segredo_de_acesso_do_twitter
```

Agora você pode rodar o codigo usando o comando abaixo

```bash
python3 -m app
```

Veja um exeplo abaixo:

```bash
GPTweeter - Bot que usa o Chat GPT para performar tweets chamativos
Qual função você quer utilizar?
1 - Postar um tweet
2 - Postar um tweet de tempo em tempo
1
Sobre qual temas você quer falar dentro dos seus tweets? (separado por virgula) Cripto Moedas
✔ Tweet Gerado com sucesso!
✔ Tweet formatado com sucesso!
✔ Tweet postado com sucesso!
Tweet publicado: "Você sabia que a criptomoeda mais valiosa do mundo é o Bitcoin? 💰 Com um valor de mercado de mais de 1 trilhão de dólares, essa moeda digital está revolucionando o mundo financeiro! #Bitcoin #criptomoedas #investimentos"
```

## Autores

- [@ojoquinhaa](https://www.github.com/ojoquinhaa)
