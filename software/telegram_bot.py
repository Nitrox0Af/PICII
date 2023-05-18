import logging
import asyncio
import threading
import os

from telegram import Update, Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler, Updater

TOKEN = '5813859429:AAH1KS33INDbN1LMa2SDALBH53WngdU2aJk'
CHAT_ID = '806031627'
reports = {}

application = ApplicationBuilder().token(TOKEN).build()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.message.from_user.first_name
    chat_id = update.effective_chat.id
    reports["chat_id"] = chat_id
    text=f"{name}, você está cadastrado(a) no sistema!"
    await context.bot.send_message(chat_id=chat_id, text=text)

async def sim(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reports["open_gate"] = True
    text=f"Você mandou SIM. O portão será ABERTA"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
    os._exit(1)

async def nao(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reports["open_gate"] = False
    text=f"Você mandou NÃO. O portão ficará FECHADA"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
    os._exit(2)

async def send_message(chat_id):
    bot = Bot(token=TOKEN)
    
    photo_path = "unknown_face/data.png" 
    await bot.send_photo(chat_id=chat_id, photo=open(photo_path, 'rb'))

    mensagem = "Essa pessoa deseja entrar. Você permite a sua entrada?\n\n- Mande /sim para ABRIR portão\n- Mande /nao para manter o portão FECHADO"
    await bot.send_message(chat_id=chat_id, text=mensagem)

def my_thread():
    asyncio.run(send_message(CHAT_ID))

def telegram_bot():
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

if __name__ == '__main__':
    telegram_bot()