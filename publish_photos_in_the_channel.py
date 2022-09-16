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
    parser.add_argument(
        '--img_per_msg',
        default=5,
        help=' count of images send into one message (default: 5 images)',
        type=int,
    )
    return parser


def collect_files(folder='.'):
    files = []
    for file_path in Path(folder).rglob('*'):
        files.append(file_path)
    return files


def fetch_images(files, pattern=('.jpg', '.png')):
    return list(filter(lambda file: file.name.endswith(pattern), files))


def create_media_group(images):
    media_group = []
    for image_path in images:
        with open(image_path, 'rb') as image:
            image = image.read()
            media_group.append(InputMediaPhoto(media=image))
    return media_group


def shuffle_images(images):
    return random.shuffle(images)


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
    media_group = create_media_group(images)

    sent_all = False
    while True:
        try:
            if sent_all:
                shuffle_images(media_group)

            chunked_media_group = list(chunked(media_group, args.img_per_msg))
            for chunk in chunked_media_group:
                send_photos_to_group(chat_id, chunk)

            sent_all = True
            time.sleep(args.frequency*3600)
        except telegram.error.NetworkError:
            print('Соединение с Интернетом не установлено')
            time.sleep(5)
