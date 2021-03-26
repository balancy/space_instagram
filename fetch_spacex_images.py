import os

import requests

SPACEX_API_URL = "https://api.spacexdata.com/v3/launches"


def find_spacex_last_launch_images_urls() -> list:
    """Finds latest launch images urls from SpaceX API.

    :return: list containing images urls
    """

    response = requests.get(SPACEX_API_URL)
    response.raise_for_status()

    response_json_format = response.json()
    for response_line in range(len(response_json_format)-1, 0, -1):
        photos_of_last_launch = response_json_format[response_line].get('links').get('flickr_images')
        if photos_of_last_launch:
            return photos_of_last_launch


def fetch_spacex_last_launch_images(folder_to_save="images/spacex/"):
    """Download SpaceX last launch images."""

    images_urls = find_spacex_last_launch_images_urls()

    for image_url in images_urls:
        physical_path_to_photo = f"{folder_to_save}{os.path.split(image_url)[1]}"

        if not os.path.exists(physical_path_to_photo):
            response = requests.get(image_url)
            if response.status_code == 404:
                continue

            with open(physical_path_to_photo, 'wb') as image:
                image.write(response.content)


if __name__ == '__main__':
    fetch_spacex_last_launch_images()
