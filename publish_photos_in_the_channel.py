import argparse
import os
import random
import time
from more_itertools import chunked

import telegram
from dotenv import load_dotenv
from telegram import InputMediaPhoto


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--frequency',
        default=4,
        help='frequency publications in hours',
        type=int,
    )
    return parser


def parse_photos(sent=False, folder='.'):
    images = []
    for root, dirs, files in os.walk(folder):
        for filename in files:
            if filename.endswith(('.jpg', '.png')):
                image_path = os.path.join(root, filename)
                images.append(InputMediaPhoto(media=open(image_path, 'rb')))
    if sent:
        random.shuffle(images)
    images = list(chunked(images, 10))

    return images


def send_photos_to_group(media):
    bot = telegram.Bot(token=TOKEN)
    bot.send_media_group(
        chat_id='@nasa0photos',
        media=media,
        timeout=100,
    )


if __name__ == '__main__':
    load_dotenv()
    parser = create_parser()
    args = parser.parse_args()

    TOKEN = os.getenv('BOT_API_TOKEN')
    sent_all = False
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
