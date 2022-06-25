import os.path
from pathlib import Path
from urllib.parse import urlsplit

import requests
from dotenv import load_dotenv


def parse_ext(url):
    path = urlsplit(url).path
    root, ext = os.path.splitext(path)
    return ext


def fetch_apod_image(url, start_date, end_date, folder='apod_images'):
    Path(folder).mkdir(exist_ok=True)
    api_key = os.getenv('API_KEY')

    payload = {
        'start_date': start_date,
        'end_date': end_date,
        'api_key': api_key,
    }

    apods = requests.get(url, params=payload)
    apods.raise_for_status()

    for index, apod in enumerate(apods.json()):
        if apod['media_type'] == 'image':
            image_url = apod.get('hdurl', apod['url'])
            response = requests.get(image_url)
            response.raise_for_status()

            image_name = f'nasa_apod_{index}{parse_ext(image_url)}'
            path = os.path.join(folder, image_name)

            with open(path, 'wb') as file:
                file.write(response.content)
                print(path)
        else:
            url = apod.get('url')
            filename = f'nasa_apod_{index}.txt'
            with open(os.path.join(folder, filename), 'w') as file:
                file.write(url)


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
    load_dotenv()
    spacex_endpoint = 'https://api.spacexdata.com/v3/launches/16'
    nasa_endpoint = 'https://api.nasa.gov/planetary/apod'
    start_date = '2022-04-20'
    end_date = '2022-05-25'

    fetch_apod_image(nasa_endpoint, start_date, end_date)
