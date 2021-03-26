import logging
import os

import requests

SPACEX_API_URL = "https://api.spacexdata.com/v3/launches"


def find_spacex_last_launch_images_urls() -> list:
    """Finds latest launch images urls from SpaceX API.

    :return: list containing images urls
    """

    response = requests.get(SPACEX_API_URL)
    response.raise_for_status()

    spacex_launches_parsed_info = response.json()
    for response_line in range(len(spacex_launches_parsed_info)-1, 0, -1):
        photos_of_last_launch = spacex_launches_parsed_info[response_line].get("links").get("flickr_images")
        if photos_of_last_launch:
            return photos_of_last_launch


def fetch_spacex_last_launch_images(folder_to_save="images/spacex/"):
    """Download SpaceX last launch images."""

    logger = logging.getLogger(__name__)

    images_urls = find_spacex_last_launch_images_urls()

    for image_url in images_urls:
        physical_path_to_photo = f"{folder_to_save}{os.path.split(image_url)[1]}"

        if not os.path.exists(physical_path_to_photo):
            response = requests.get(image_url)
            if not response.ok:
                logger.warning(f"Unable to reach url {image_url}")
                continue

            with open(physical_path_to_photo, "wb") as image:
                image.write(response.content)


if __name__ == "__main__":
    fetch_spacex_last_launch_images()
