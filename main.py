from telegram.ext import Updater
from telegram.ext import CommandHandler
import telegram
import requests
from random import choice
import os

def main():
    token='1467163688:AAFdWLBrFIGP9IABB3im2mZtO6qkWjlNYvA'
    url = 'https://villydictbot.herokuapp.com/'
    PORT = int(os.environ.get('PORT', '5000'))

    updater=Updater(use_context=True,token=token)
   
    dispatcher = updater.dispatcher

    bot = telegram.Bot(token = token)
    bot.setWebhook(url + token)

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    defina_handler = CommandHandler('defina', defina)
    dispatcher.add_handler(defina_handler)
    
    updater.start_webhook(listen="0.0.0.0",
                            port=int(PORT),
                            url_path=token)
    updater.bot.setWebhook(url + token)

    updater.idle()

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

def defina(update, context):
    req=requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/pt-BR/{context.args}").json()
    aux=[]
    try:
        for i in req[0].get('meanings','Sem definição')[0].get('definitions'): 
            aux.append(i.get('definition')) 
        context.bot.send_message(chat_id=update.effective_chat.id, text=choice(aux))    
    except Exception as err:
        context.bot.send_message(chat_id=update.effective_chat.id, text='Não encontrei D:') 

if __name__ == '__main__':
    main()



