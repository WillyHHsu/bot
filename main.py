import os
import sys
import requests
import logging
from telegram.ext import Updater
from telegram.ext import CommandHandler
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

logger = logging.getLogger()

MODE = os.getenv("MODE", 'dev')
TOKEN = os.getenv("TOKEN")
PORT = int(os.environ.get("PORT", "8443"))
HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME")

updater = Updater(token=TOKEN, use_context=True)

dispatcher = updater.dispatcher


def run(updater):
    if MODE == "dev":
        updater.start_polling()
    elif MODE == "prod":
        updater.start_webhook(listen="0.0.0.0",
                              port=PORT,
                              url_path=TOKEN)
        updater.bot.set_webhook(
            f"https://{HEROKU_APP_NAME}.herokuapp.com/{TOKEN}")
        updater.idle()
    else:
        logger.error("No MODE specified!")
        sys.exit(1)


def start(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="I will try to explain all the things in the universe."
    )


def help_command(update: Update, context: CallbackContext) -> None:
    help_text = '''
/define [term, lang=en-US]
Get a explain about `term`.

/defina [termo, lang=pt-BR]
Responde a mensagem com a definição do termo
'''
    update.message.reply_text(text=help_text, parse_mode=ParseMode.MARKDOWN)
def define(term, lang='en-US'):
    try:
        req = requests.get(
            f"https://api.dictionaryapi.dev/api/v2/entries/{lang}/{term}").json()
        definitions = "\n".join(
            [f'{i[0]+1}º: {i[1]}' for i in enumerate(
                i['definition'] for i in req[0]['meanings'][0]['definitions'])]
        )
        logger.info(f"define {term} with lang {lang}")
        return f"{str.capitalize(term)}:\n{definitions}"
    except (
        IndexError,  # Não retornou o formato esperado
        KeyError,   # ...
        TypeError   # ...
    ):
        return False
    except (
        requests.exceptions.Timeout,
        requests.exceptions.TooManyRedirects,
        requests.exceptions.RequestException
    ) as e:
        logger.error(f"Erro: {e}")
        return str(e)


def defina(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=define(' '.join(context.args),
                    lang='pt-BR') or "Não sei explicar."
    )


def meaning(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=define(' '.join(context.args)) or "I do not know how to explain.",
    )


if __name__ == '__main__':
    logger.info("Starting bot")
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('defina', defina))
    dispatcher.add_handler(CommandHandler('meaning', meaning))
    run(updater)
