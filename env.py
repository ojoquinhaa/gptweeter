from os import getenv
from dotenv import load_dotenv

# Carregar as variáveis de ambiente do arquivo .env
load_dotenv()

# Acessar as variáveis de ambiente
OPENAI_API_KEY = getenv("OPENAI_API_KEY")
CONSUMER_KEY = getenv("CONSUMER_KEY")
CONSUMER_SECRET = getenv("CONSUMER_SECRET")
ACCESS_TOKEN = getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = getenv("ACCESS_TOKEN_SECRET")
BEARER_TOKEN = getenv("BEARER_TOKEN")
