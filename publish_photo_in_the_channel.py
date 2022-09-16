import argparse
import os
import random
from pathlib import Path

import telegram
from dotenv import load_dotenv


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--photo',
        default=None,
        type=str,
    )
    return parser


def collect_files(folder='.'):
    files = []
    for file_path in Path(folder).rglob('*'):
        files.append(file_path)
    return files


def filter_files(files, pattern=('.jpg', '.png')):
    return list(filter(lambda file: file.name.endswith(pattern), files))


def filter_photos(photos, photo_name):
    for photo in photos:
        if photo.name.startswith(photo_name):
            return photo


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

    if bot:
        all_files = collect_files()
        photos = filter_files(all_files)
        if args.photo:
            required_photo = filter_photos(photos, args.photo)
            try:
                send_photo_to_group(
                    chat_id,
                    img_path=required_photo.as_posix(),
                )
            except telegram.error.BadRequest:
                print('Фото с таким именем не существует')
        else:
            random_photo = random.choice(photos)
            send_photo_to_group(chat_id, img_path=random_photo.as_posix())
