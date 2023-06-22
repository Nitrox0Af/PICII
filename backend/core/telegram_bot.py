import logging
import os
import requests

from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes


TOKEN = '5813859429:AAH1KS33INDbN1LMa2SDALBH53WngdU2aJk'

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

application = ApplicationBuilder().token(TOKEN).build()


def main():
    start_handler = CommandHandler('start', start)
    get_message_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), get_message)

    application.add_handler(start_handler)
    application.add_handler(get_message_handler)
        
    application.run_polling()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler function for the /start command"""
    name = update.message.from_user.first_name
    text=f"{name}, informe o seu e-mail para ser cadastrado(a) no sistema"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)


async def get_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler function for text messages"""
    chat_id = update.effective_chat.id
    message_received = update.message.text.strip().replace(" ", "").replace("-", "").replace(".", "").replace("_", "")
    if set_chat_id(message_received, chat_id):
        text = "Você foi cadastrado com sucesso"
        await context.bot.send_message(chat_id=chat_id, text=text)
        os._exit(1)
    else:
        message_received = "E-mail inválido. Tente novamente"
        await context.bot.send_message(chat_id=chat_id, text=message_received)


def set_chat_id(email: str, chat_id: str):
    """Set the chat_id"""
    url = f'http://10.9.10.17:8000/owner/json/{email}/'  
    data = {
        'chat_id': chat_id
    }
    response = requests.post(url, data=data)

    if response.status_code == 200:
        return True
    else:
        return False


if __name__ == '__main__':
    main()