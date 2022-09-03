import argparse
import os.path
from pathlib import Path

import requests
from dotenv import load_dotenv


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--launch_id',
        default='next',
        help='launch number (default: latest launch)',
    )
    return parser


def fetch_spacex_last_launch(launch_id, folder='images'):
    spacex_endpoint = f'https://api.spacexdata.com/v3/launches/{launch_id}'

    Path(folder).mkdir(exist_ok=True)
    spacex_response = requests.get(spacex_endpoint)
    spacex_response.raise_for_status()

    launch_image_links = spacex_response.json()['links']['flickr_images']

    for index, launch_image_link in enumerate(launch_image_links, 1):
        launch_image_response = requests.get(launch_image_link)
        launch_image_response.raise_for_status()

        filename = f'spacex{index}.jpg'
        path = os.path.join(folder, filename)

        with open(path, 'wb') as file:
            file.write(launch_image_response.content)


if __name__ == '__main__':
    load_dotenv()
    parser = create_parser()
    args = parser.parse_args()

    fetch_spacex_last_launch(args.launch_id)
