import argparse
import os
import random
import time

import telegram
from dotenv import load_dotenv
from more_itertools import chunked
from telegram import InputMediaPhoto

from funcs import collect_files, fetch_images


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--frequency',
        default=4,
        help='frequency publications in hours (default: 4 hours)',
        type=int,
    )
    parser.add_argument(
        '--img_per_msg',
        default=5,
        help=' count of images send into one message (default: 5 images)',
        type=int,
    )
    return parser


def create_media_group(images):
    media_group = []
    for image_path in images:
        with open(image_path, 'rb') as image:
            image = image.read()
            media_group.append(InputMediaPhoto(media=image))
    return media_group


def send_photos_to_group(chat_id, media):
    bot.send_media_group(
        chat_id=chat_id,
        media=media,
        timeout=100,
    )


if __name__ == '__main__':
    load_dotenv()
    parser = create_parser()
    args = parser.parse_args()

    tg_bot_token = os.environ['TG_BOT_TOKEN']
    bot = telegram.Bot(token=tg_bot_token)

    chat_id = os.environ['TG_CHAT_ID']

    all_files = collect_files()
    images = fetch_images(all_files)

    while True:
        media_group = create_media_group(images)
        try:
            chunked_media_group = list(chunked(media_group, args.img_per_msg))
            for chunk in chunked_media_group:
                send_photos_to_group(chat_id, chunk)

            random.shuffle(images)
            time.sleep(args.frequency)
        except telegram.error.NetworkError:
            print('Соединение с Интернетом не установлено')
            time.sleep(5)
