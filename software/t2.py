from telethon import TelegramClient

api_id = 20447974  # Substitua pelo seu api_id
api_hash = "8657411eb429d1a7571069696b36b812"  # Substitua pelo seu api_hash

client = TelegramClient('teste', api_id, api_hash)

async def send_message():
    # Inicie o cliente Telegram
    await client.start()

    # Enviar a mensagem
    await client.send_message('Nitrox_af', 'Olá, esta é uma mensagem enviada pelo meu bot do Telegram.')

    # Encerre o cliente Telegram
    await client.disconnect()

# Execute a função assíncrona
with client:
    client.loop.run_until_complete(send_message())
