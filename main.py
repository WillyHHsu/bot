import os
import sys
import requests
import logging
from telegram.ext import Updater
from telegram.ext import CommandHandler
from random import choice
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

MODE = os.getenv("MODE", 'dev')
TOKEN = os.getenv("TOKEN")
if MODE == "dev":
    def run(updater):
        updater.start_polling()
elif MODE == "prod":
    def run(updater):
        PORT = int(os.environ.get("PORT", "8443"))
        HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME")
        updater.start_webhook(listen="0.0.0.0",
                              port=PORT,
                              url_path=TOKEN)
        updater.bot.set_webhook(
            "https://{}.herokuapp.com/{}".format(HEROKU_APP_NAME, TOKEN))
else:
    logger.error("No MODE specified!")
    sys.exit(1)

updater = Updater(token=TOKEN, use_context=True)

dispatcher = updater.dispatcher


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


def define(term, lang='en-US'):
    try:
        req = requests.get(
            f"https://api.dictionaryapi.dev/api/v2/entries/{lang}/{term}").json()
        definitions = "\n".join(
            [f'{i[0]+1}º: {i[1]}' for i in enumerate(
                i['definition'] for i in req[0]['meanings'][0]['definitions'])]
        )
        return f"{str.capitalize(term)}:\n{definitions}"
    except (
        requests.exceptions.Timeout,
        requests.exceptions.TooManyRedirects,
        requests.exceptions.RequestException,
        IndexError,  # Não retornou o formato esperado
        KeyError,   # ...
        TypeError   # ...
    ) as e:
        return 'Falhei misera D:', e, term, lang


def defina(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=define(' '.join(context.args), lang='pt-BR')
    )


def meaning(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=define(' '.join(context.args))
    )

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

defina_handler = CommandHandler('defina', defina)
dispatcher.add_handler(defina_handler)

meaning_handler = CommandHandler('meaning', meaning)
dispatcher.add_handler(meaning_handler)
    
updater.start_polling()
