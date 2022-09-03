import argparse
import os
import random

import telegram
from dotenv import load_dotenv


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--photo',
        default='nasa_apod_1',
        type=str,
    )
    return parser


def parse_photos(image_name=None, folder='.'):
    images = []
    for root, dirs, files in os.walk(folder):
        for filename in files:
            if filename.endswith(('.jpg', '.png')) and not image_name:
                image_path = os.path.join(root, filename)
                images.append(open(image_path, 'rb'))
            elif image_name:
                if filename.endswith(('.jpg', '.png')) \
                        and filename.startswith(image_name):
                    return os.path.join(root, filename)
    return images


def send_photo_to_group(photo=None, path=None):
    bot = telegram.Bot(token=TG_BOT_TOKEN)
    if path:
        bot.send_photo(
            chat_id=chat_id,
            photo=open(path, 'rb'),
            timeout=100,
        )
    else:
        bot.send_photo(
            chat_id=chat_id,
            photo=photo,
            timeout=100,
        )


if __name__ == '__main__':
    load_dotenv()
    parser = create_parser()
    args = parser.parse_args()

    try:
        TG_BOT_TOKEN = os.environ['TG_BOT_TOKEN']
    except KeyError:
        print('Укажите TG_BOT_TOKEN в .env')

    chat_id = os.getenv('TG_CHAT_ID', '@nasa0photos')

    if args.photo:
        image_path = parse_photos(image_name=args.photo)
        try:
            send_photo_to_group(path=image_path)
        except telegram.error.BadRequest:
            print('Фото с таким именем не существует')
    else:
        parsed_photo = random.choice(parse_photos())
        send_photo_to_group(photo=parsed_photo)
