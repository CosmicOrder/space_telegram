import requests


def download_image(url):
    response = requests.get(url)
    response.raise_for_status()

    filename = 'hubble.jpeg'

    with open(filename, 'wb') as file:
        file.write(response.content)


if __name__ == '__main__':
    url = 'https://upload.wikimedia.org/wikipedia/commons/3/3f/HST-SM4.jpeg'
    download_image(url)
