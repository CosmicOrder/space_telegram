import argparse
import os.path
from datetime import datetime
from pathlib import Path

import requests
from dotenv import load_dotenv


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--number_of_photos',
        default=5,
        type=int,
    )
    return parser


def fetch_epic_images(quantity, folder='epic_images'):
    epic_endpoint = 'https://api.nasa.gov/EPIC/api/natural'
    epic_picture_url = 'https://api.nasa.gov/EPIC/archive/natural/'

    Path(folder).mkdir(exist_ok=True)
    api_key = os.getenv('NASA_API_KEY')

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

        epic_response = requests.get(epic_url, params=payload)
        epic_response.raise_for_status()

        filename = f'epic{index}.png'
        path = os.path.join(folder, filename)

        with open(path, 'wb') as file:
            file.write(epic_response.content)


if __name__ == '__main__':
    load_dotenv()
    parser = create_parser()
    args = parser.parse_args()
    quantity = args.number_of_photos

    fetch_epic_images(quantity)
