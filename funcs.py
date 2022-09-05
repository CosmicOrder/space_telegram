from pathlib import Path

import requests


def fetch_and_save_photos(
        url,
        api_name,
        index,
        folder,
        img_url=' .jpg',
        payload='',
):
    response = requests.get(url, params=payload)
    response.raise_for_status()

    filename = f'{api_name}{index}{Path(img_url).suffix}'
    path = Path(folder, filename)

    with open(path, 'wb') as file:
        file.write(response.content)
        print(path)