import argparse
import os.path
from pathlib import Path
from urllib.parse import urlsplit

import requests
from dotenv import load_dotenv


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--start_date',
        default='2022-01-01',
    )
    parser.add_argument(
        '--end_date',
        default='2022-01-05',
    )
    return parser


def parse_ext(url):
    path = urlsplit(url).path
    root, ext = os.path.splitext(path)
    return ext


def fetch_apod_images(url, start_date, end_date, folder='apod_images'):
    Path(folder).mkdir(exist_ok=True)
    api_key = os.getenv('API_KEY')

    payload = {
        'start_date': start_date,
        'end_date': end_date,
        'api_key': api_key,
    }

    apods = requests.get(url, params=payload)
    apods.raise_for_status()

    for index, apod in enumerate(apods.json(), 1):
        if apod['media_type'] == 'image':
            image_url = apod.get('hdurl', apod['url'])
            apod_response = requests.get(image_url)
            apod_response.raise_for_status()

            image_name = f'nasa_apod_{index}{parse_ext(image_url)}'
            path = os.path.join(folder, image_name)

            with open(path, 'wb') as file:
                file.write(apod_response.content)
                print(path)
        else:
            url = apod.get('url')
            filename = f'nasa_apod_{index}.txt'
            path = os.path.join(folder, filename)
            with open(path, 'w') as file:
                file.write(url)


if __name__ == '__main__':
    load_dotenv()
    parser = create_parser()
    args = parser.parse_args()

    apod_endpoint = 'https://api.nasa.gov/planetary/apod'
    start_date = args.start_date
    end_date = args.end_date

    fetch_apod_images(apod_endpoint, start_date, end_date)
