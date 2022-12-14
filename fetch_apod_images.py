import argparse
import os.path

import requests
from dotenv import load_dotenv

from funcs import fetch_and_save_photos


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--start_date',
        default='2022-01-01',
        help='The start of the date range (default: 2022-01-01)',
    )
    parser.add_argument(
        '--end_date',
        default='2022-01-05',
        help='The end of the date range (default: 2022-01-05)',
    )
    return parser


def fetch_apod_images(start_date, end_date, folder='apod_images'):
    apod_endpoint = 'https://api.nasa.gov/planetary/apod'

    payload = {
        'start_date': start_date,
        'end_date': end_date,
        'api_key': api_key,
    }

    apods = requests.get(apod_endpoint, params=payload)
    apods.raise_for_status()

    for index, apod in enumerate(apods.json(), 1):
        if apod['media_type'] == 'image':
            image_url = apod.get('hdurl', apod['url'])

            fetch_and_save_photos(
                image_url,
                api_name='apod',
                index=index,
                folder=folder,
                img_url=image_url,
            )


if __name__ == '__main__':
    load_dotenv()
    parser = create_parser()
    args = parser.parse_args()

    start_date = args.start_date
    end_date = args.end_date

    api_key = os.environ['NASA_API_KEY']

    fetch_apod_images(start_date, end_date)
