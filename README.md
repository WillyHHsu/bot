# Telegram Bot

Este filho de Willy foi criado para ser um **dicionario**

## How to

### Faça um arquivo chamado `.env` contendo as seguintes váriaveis de ambiente: 

```
TOKEN=your_token
MODE=dev
```

### Seu ambiente de produção deve ter as seguintes váriaveis: (HEROKU)

```
TOKEN=token_forncecido_pelo_botfather
MODE=prod
HEROKU_APP_NAME=nome_da_sua_aplicação
POETRY_VERSION=1.1.4 # Necessário se utilizar o buildpack para poetry
PYTHON_RUNTIME_VERSION=3.8.8 # Necessário se utilizar o buildpack para poetry
```

* Você também pode utilizar o seguinte buildpack para as dependências com poetry:

    * https://github.com/moneymeets/python-poetry-buildpack.git

* Você também pode usar o requirements.txt deste projeto ou ainda pode gerar um arquivo requirements.txt a partir do poetry com:

    * `poetry export -f requirements.txt --output requirements.txt`

---
## Python Telegram Bot doc

> https://python-telegram-bot.readthedocs.io/en/stable/
## Get telegram bot token 

> https://core.telegram.org/bots#6-botfather

* BotFather on Telegram 
    > https://telegram.me/botfather

Update your `.env` file with your new TOKEN