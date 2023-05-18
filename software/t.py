from telegram import Bot
import asyncio

# Token do bot do Telegram
TOKEN = '5813859429:AAH1KS33INDbN1LMa2SDALBH53WngdU2aJk'

# ID do chat ou do usuário para onde a mensagem será enviada
CHAT_ID = '806031627'

# Função assíncrona para enviar a mensagem
async def send_message():
    # Crie uma instância do bot
    bot = Bot(token=TOKEN)
    
    mensagem = 'Olá, esta é uma mensagem enviada pelo meu bot do Telegram.'

    # Envie a mensagem para o chat
    await bot.send_message(chat_id=chat_id, text=mensagem)

# Execute a função assíncrona
asyncio.run(send_message())


# import telegram


# async def main():
#     bot = telegram.Bot(TOKEN)
#     async with bot:
#         print(await bot.get_me())


# if __name__ == '__main__':
#     asyncio.run(main())