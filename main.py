import os.path
from datetime import datetime
from pathlib import Path
from urllib.parse import urlsplit

import requests
from dotenv import load_dotenv


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

    for index, apod in enumerate(apods.json()):
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


def fetch_spacex_last_launch(url, folder='images/'):
    Path(folder).mkdir(exist_ok=True)
    spacex_response = requests.get(url)
    spacex_response.raise_for_status()

    launch_image_links = spacex_response.json()['links']['flickr_images']

    for index, launch_image_link in enumerate(launch_image_links, 1):
        launch_image_response = requests.get(launch_image_link)
        launch_image_response.raise_for_status()

        filename = f'spacex{index}.jpg'
        path = os.path.join(folder, filename)

        with open(path, 'wb') as file:
            file.write(launch_image_response.content)


def fetch_epic_images(url, epic_picture_url, folder='epic_images'):
    Path(folder).mkdir(exist_ok=True)
    api_key = os.getenv('API_KEY')

    payload = {
        'api_key': api_key,
    }
    epics = requests.get(url, params=payload)
    epics.raise_for_status()

    epics = epics.json()[:5]

    for index, epic in enumerate(epics, 1):
        image = epic['image']
        date = datetime.fromisoformat(epic['date']).strftime("%Y/%d/%m")
        epic_url = f'{epic_picture_url}{date}/png/{image}.png'

        epic_response = requests.get(epic_url, params=payload)
        epic_response.raise_for_status()

        filename = f'epic{index}.png'
        path = os.path.join(folder, filename)

        with open(path, 'wb') as file:
            file.write(epic_response.content)


if __name__ == '__main__':
    load_dotenv()

    spacex_endpoint = 'https://api.spacexdata.com/v3/launches/16'
    nasa_endpoint = 'https://api.nasa.gov/planetary/apod'
    epic_endpoint = 'https://api.nasa.gov/EPIC/api/natural'
    epic_picture_url = 'https://api.nasa.gov/EPIC/archive/natural/'
    start_date = '2022-04-20'
    end_date = '2022-05-25'

    fetch_epic_images(epic_endpoint, epic_picture_url)
    fetch_apod_images(nasa_endpoint, start_date, end_date)
    fetch_spacex_last_launch(spacex_endpoint)
