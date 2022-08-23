import os

import telegram
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('BOT_API_TOKEN')

bot = telegram.Bot(token=TOKEN)
bot.send_photo(
    chat_id='@nasa0photos',
    photo=open('images/spacex1.jpg', 'rb'),
)
