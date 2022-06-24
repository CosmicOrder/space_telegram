import os.path
from pathlib import Path

import requests


def fetch_spacex_last_launch(url, folder='images/'):
    Path(folder).mkdir(exist_ok=True)
    response = requests.get(url)
    response.raise_for_status()

    image_links = response.json()['links']['flickr_images']

    for index, image_link in enumerate(image_links, 1):
        response = requests.get(image_link)
        response.raise_for_status()

        filename = f'spacex{index}.jpg'
        path = os.path.join(folder, filename)

        with open(path, 'wb') as file:
            file.write(response.content)


if __name__ == '__main__':
    endpoint_url = 'https://api.spacexdata.com/v3/launches/16'

    fetch_spacex_last_launch(endpoint_url)
