import os

import telegram
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('BOT_API_TOKEN')

bot = telegram.Bot(token=TOKEN)
bot.send_message(
    chat_id='@nasa0photos',
    text='Привет, подписчики!',
)
