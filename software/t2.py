import logging
import asyncio
from telegram import Update, Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    CallbackQueryHandler,
)

TOKEN = '5813859429:AAH1KS33INDbN1LMa2SDALBH53WngdU2aJk'

reports = {}

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.message.from_user.first_name
    chat_id = update.effective_chat.id
    reports["chat_id"] = chat_id
    text = f"{name}, você está cadastrado(a) no sistema!"

    # Criação dos botões "Sim" e "Não"
    keyboard = [
        [InlineKeyboardButton("Sim", callback_data="sim"),
         InlineKeyboardButton("Não", callback_data="nao")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup)

async def send_message(chat_id):
    # Crie uma instância do bot
    bot = Bot(token=TOKEN)
    
    mensagem = "Essa pessoa deseja entrar. Você quer abriar a porta?"
    photo_path = "unknown_face/data.png"  # Insira o caminho completo da foto

    keyboard = [
        [InlineKeyboardButton("Sim", callback_data='sim')],
        [InlineKeyboardButton("Não", callback_data='nao')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Envie a foto para o chat
    await bot.send_photo(chat_id=chat_id, photo=open(photo_path, 'rb'))

    # Envie a mensagem para o chat
    await bot.send_message(chat_id=chat_id, text=mensagem)


async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    chat_id = query.message.chat_id
    data = query.data

    if data == "sim":
        await context.bot.send_message(chat_id=chat_id, text="Você escolheu 'Sim'!")
    elif data == "nao":
        await context.bot.send_message(chat_id=chat_id, text="Você escolheu 'Não'!")

if __name__ == '__main__':

    application = ApplicationBuilder().token(TOKEN).build()

    start_handler = CommandHandler('start', start)
    button_handler = CallbackQueryHandler(button_click)

    application.add_handler(start_handler)
    
    application.add_handler(button_handler)

    application.run_polling()

    asyncio.run(send_message("806031627"))
