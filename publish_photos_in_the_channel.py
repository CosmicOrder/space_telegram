import argparse
import os
import random
import time
from pathlib import Path

from more_itertools import chunked

import telegram
from dotenv import load_dotenv
from telegram import InputMediaPhoto


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--frequency',
        default=4,
        help='frequency publications in hours (default: 4 hours)',
        type=int,
    )
    return parser


def parse_photos(sent=False, folder='.'):
    images = []
    for root, dirs, files in os.walk(folder):
        for filename in files:
            if filename.endswith(('.jpg', '.png')):
                image_path = Path(root, filename)
                with open(image_path, 'rb') as image:
                    image = image.read()
                images.append(InputMediaPhoto(media=image))
    if sent:
        random.shuffle(images)
    images = list(chunked(images, 10))

    return images


def send_photos_to_group(media):
    bot.send_media_group(
        chat_id=chat_id,
        media=media,
        timeout=100,
    )


if __name__ == '__main__':
    load_dotenv()
    parser = create_parser()
    args = parser.parse_args()

    TG_BOT_TOKEN = os.environ['TG_BOT_TOKEN']
    bot = telegram.Bot(token=TG_BOT_TOKEN)

    chat_id = os.getenv('TG_CHAT_ID', '@nasa0photos')

    sent_all = False
    if bot:
        while True:
            try:
                if sent_all:
                    parsed_photos = parse_photos(sent_all)
                else:
                    parsed_photos = parse_photos()
                for some_parsed_photo in parsed_photos:
                    send_photos_to_group(some_parsed_photo)
                sent_all = True
                time.sleep(args.frequency*3600)
            except telegram.error.NetworkError:
                print('Соединение с Интернетом не установлено')
                time.sleep(5)
