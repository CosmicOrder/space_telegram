import argparse
import os.path
from datetime import datetime

import requests
from dotenv import load_dotenv

from funcs import fetch_and_save_photos


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--number_of_photos',
        default=5,
        help='number of photos (default: 5)',
        type=int,
    )
    return parser


def fetch_epic_images(quantity, folder='epic_images'):
    epic_endpoint = 'https://api.nasa.gov/EPIC/api/natural'
    epic_picture_url = 'https://api.nasa.gov/EPIC/archive/natural/'

    payload = {
        'api_key': api_key,
    }
    epics = requests.get(epic_endpoint, params=payload)
    epics.raise_for_status()

    epics = epics.json()[:quantity]

    for index, epic in enumerate(epics, 1):
        image = epic['image']
        date = datetime.fromisoformat(epic['date']).strftime("%Y/%m/%d")
        epic_url = f'{epic_picture_url}{date}/png/{image}.png'

        fetch_and_save_photos(
            epic_url,
            api_name='epic',
            index=index,
            folder=folder,
            img_url=epic_url,
            payload=payload,
        )


if __name__ == '__main__':
    load_dotenv()
    parser = create_parser()
    args = parser.parse_args()

    quantity = args.number_of_photos

    api_key = os.environ['NASA_API_KEY']

    fetch_epic_images(quantity)
