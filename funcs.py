from pathlib import Path

import requests


def fetch_and_save_photos(
        url,
        api_name,
        index,
        folder,
        img_url=' .jpg',
        payload=None,
):
    Path(folder).mkdir(exist_ok=True)
    response = requests.get(url, params=payload)
    response.raise_for_status()

    filename = f'{api_name}{index}{Path(img_url).suffix}'
    path = Path(folder, filename)

    with open(path, 'wb') as file:
        file.write(response.content)
        print(path)


def collect_files(folder='.'):
    return [file_path for file_path in Path(folder).rglob('*')]


def fetch_images(files, pattern=('.jpg', '.png')):
    return list(filter(lambda file: file.name.endswith(pattern), files))
