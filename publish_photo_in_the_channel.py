import argparse
import os
import random

import telegram
from dotenv import load_dotenv

from funcs import collect_files, fetch_images


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--photo',
        default=None,
        type=str,
    )
    return parser


def choose_image(images, photo_name):
    for image in images:
        if image.name.startswith(photo_name):
            return image


def send_photo_to_group(chat_id, img_path=None):
    with open(img_path, 'rb') as image:
        image = image.read()

    bot.send_photo(
        chat_id=chat_id,
        photo=image,
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
    if args.photo:
        photo = choose_image(images, args.photo)
    else:
        photo = random.choice(images)
    try:
        send_photo_to_group(chat_id, img_path=photo.as_posix())
    except AttributeError:
        print('Фото с таким именем не существует')
