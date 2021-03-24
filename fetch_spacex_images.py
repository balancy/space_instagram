import os

import requests

SPACEX_API_URL = "https://api.spacexdata.com/v3/launches"


def find_spacex_last_launch_images_urls() -> list:
    """Finds latest launch images urls from SpaceX API.

    :return: list containing images urls
    """

    response = requests.get(SPACEX_API_URL)
    response.raise_for_status()

    for response_line in range(len(response.json())-1, 0, -1):
        photos_of_last_launch = response.json()[response_line].get('links').get('flickr_images')
        if photos_of_last_launch:
            return photos_of_last_launch


def fetch_spacex_last_launch_images(folder_to_save="images/spacex/"):
    """Download SpaceX last launch images.
    """

    paths_to_images = []
    images_urls = find_spacex_last_launch_images_urls()

    for image_url in images_urls:
        physical_path_to_photo = f"{folder_to_save}{image_url.split('/')[-1]}"

        if not os.path.exists(physical_path_to_photo):
            response = requests.get(image_url)
            try:
                response.raise_for_status()
            except requests.HTTPError:
                continue

            with open(physical_path_to_photo, 'wb') as image:
                image.write(response.content)

        paths_to_images.append(physical_path_to_photo)


if __name__ == '__main__':
    fetch_spacex_last_launch_images()
