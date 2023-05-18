import logging
import asyncio
import threading
import os
import sys

from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler


TOKEN = '5813859429:AAH1KS33INDbN1LMa2SDALBH53WngdU2aJk'
CHAT_ID = '806031627'
args = sys.argv
reports = {}

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

application = ApplicationBuilder().token(TOKEN).build()


def main():
    thread = threading.Thread(target=my_thread)
    thread.start()
    thread.join()

    start_handler = CommandHandler('start', start)
    sim_handler = CommandHandler('sim', sim)
    nao_handler = CommandHandler('nao', nao)

    application.add_handler(start_handler)
    application.add_handler(sim_handler)
    application.add_handler(nao_handler)
        
    application.run_polling()


def my_thread():
    person = args[1]
    asyncio.run(send_message(CHAT_ID, person))


async def send_message(chat_id: str, person: str):
    bot = Bot(token=TOKEN)
    
    photo_path = "unknown_face/data.png" 
    await bot.send_photo(chat_id=chat_id, photo=open(photo_path, 'rb'))

    person = "Essa pessoa" if person == "unknown" else person
    mensagem = f"{person} deseja entrar. Você permite a sua entrada?\n\n- Mande /sim para ABRIR portão\n- Mande /nao para manter o portão FECHADO"
    await bot.send_message(chat_id=chat_id, text=mensagem)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.message.from_user.first_name
    chat_id = update.effective_chat.id
    reports["chat_id"] = chat_id
    text=f"{name}, você está cadastrado(a) no sistema!"
    await context.bot.send_message(chat_id=chat_id, text=text)


async def sim(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text=f"Você mandou SIM. O portão será ABERTO"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
    os._exit(1)


async def nao(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text=f"Você mandou NÃO. O portão ficará FECHADO"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
    os._exit(2)


if __name__ == '__main__':
    main()