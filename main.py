import os.path
from pathlib import Path

import requests


def download_image(url, folder='images/'):
    Path(folder).mkdir(exist_ok=True)
    response = requests.get(url)
    response.raise_for_status()

    return print(response.json()['links']['flickr_images'])


if __name__ == '__main__':
    endpoint_url = 'https://api.spacexdata.com/v3/launches/16'

    download_image(endpoint_url)
