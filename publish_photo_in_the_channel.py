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


def fetch_images(files, pattern=('.jpg', '.png')):
    return list(filter(lambda file: file.name.endswith(pattern), files))


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
        required_photo = choose_image(images, args.photo)
        if required_photo:
            send_photo_to_group(
                chat_id,
                img_path=required_photo.as_posix(),
            )
        else:
            print('Картинка с таким именем не существует')
    else:
        random_photo = random.choice(images)
        send_photo_to_group(chat_id, img_path=random_photo.as_posix())
