import os

import requests

SPACEX_API_URL = "https://api.spacexdata.com/v3/launches"
HUBBLE_API_URL = "http://hubblesite.org/api/v3/image/"


def check_folder(folder='images/') -> None:
    """Checks if folder exists. If not, creates it.

    :param folder: relative path to folder
    """
    if not os.path.exists(folder):
        os.makedirs(folder)


def find_spacex_last_launch_images_urls() -> list:
    """Finds latest launch images urls from SpaceX API.

    :return: list containing images urls
    """

    r = requests.get(SPACEX_API_URL)
    r.raise_for_status()

    for i in range(len(r.json())-1, 0, -1):
        photos_of_last_launch = r.json()[i].get('links').get('flickr_images')
        if photos_of_last_launch:
            return photos_of_last_launch


def download_images_from_urls(images_urls, folder='images/spacex/') -> None:
    """Download images from urls given in a list.

    :param images_urls: list of images urls
    :param folder: folder to save images
    """

    check_folder(folder)

    for image_url in images_urls:
        r = requests.get(image_url)
        r.raise_for_status()

        physical_path_to_photo = f"{folder}{image_url.split('/')[-1]}"
        with open(physical_path_to_photo, 'wb') as image:
            image.write(r.content)


def fetch_hubble_image_by_id(image_id, folder='images/hubble/') -> None:
    """Finds hubble best quality image bu its id and download it.

    :param image_id: id of the image
    :param folder: folder to save image
    """

    check_folder(folder)

    r = requests.get(f"{HUBBLE_API_URL}{image_id}", verify=False)
    r.raise_for_status()

    image_url = f"https:{r.json().get('image_files')[-1].get('file_url')}"
    r = requests.get(image_url, verify=False)
    r.raise_for_status()

    physical_path_to_photo = f"{folder}{image_id}.{image_url.split('.')[-1]}"
    with open(physical_path_to_photo, 'wb') as image:
        image.write(r.content)


if __name__ == '__main__':
    requests.packages.urllib3.disable_warnings()

    try:
        images_urls = find_spacex_last_launch_images_urls()
        download_images_from_urls(images_urls)
        fetch_hubble_image_by_id(1)
    except requests.HTTPError:
        pass
