import os
import sys
import requests
import logging
from telegram import ParseMode, Update
from telegram.ext import Updater, CommandHandler, CallbackContext
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


def get_define(term, lang='en-US'):
    logger.info(f"define {term} with lang {lang}")
    try:
        req = requests.get(
            f"https://api.dictionaryapi.dev/api/v2/entries/{lang}/{term}").json()
        definitions = "\n".join(
            [f'*{i[0]+1}º - * {i[1]}' for i in enumerate(
                i['definition'] for i in req[0]['meanings'][0]['definitions'])]
        )
        return f"_{str.capitalize(term)}_:\n\n{definitions}"
    except (
        IndexError,
        KeyError,
        TypeError
    ):   # Não retornou o formato esperado
        return False
    except (
        requests.exceptions.Timeout,
        requests.exceptions.TooManyRedirects,
        requests.exceptions.RequestException
    ) as e:
        logger.error(f"Erro: {e}")
        return str(e)


def define(update, context, not_found_msg="I do not know how to explain."):
    term, *lang = ' '.join(context.args).split(',')
    text = get_define(term, lang[0].strip()
                      if lang else 'en-US') or not_found_msg
    message = update.effective_message
    message.reply_text(
        text,
        reply_to_message_id=message["message_id"],
        parse_mode=ParseMode.MARKDOWN
    )


def defina(update, context):
    context.args.append(',pt-BR')
    define(update, context, not_found_msg="Não sei explicar")


if __name__ == '__main__':
    logger.info("Starting bot")
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('help', help_command))
    dispatcher.add_handler(CommandHandler('define', define))
    dispatcher.add_handler(CommandHandler('defina', defina))
    run(updater)
