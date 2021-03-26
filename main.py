import logging
import os

from dotenv import load_dotenv
import requests

from fetch_hubble_images import fetch_hubble_images_by_collection
from fetch_spacex_images import fetch_spacex_last_launch_images
from post_instagram import post_images_on_instagram
from resize_images import reformat_images_instagram_format


if __name__ == "__main__":
    requests.packages.urllib3.disable_warnings()
    load_dotenv()
    logging.basicConfig(level=logging.INFO)

    hubble_images_folder = "images/hubble/"
    spacex_images_folder = "images/spacex/"
    insta_images_folder = "images/instagram/"

    os.makedirs(spacex_images_folder, exist_ok=True)
    os.makedirs(hubble_images_folder, exist_ok=True)
    os.makedirs(insta_images_folder, exist_ok=True)

    try:
        fetch_spacex_last_launch_images(spacex_images_folder)
    except requests.HTTPError:
        logging.error("SpaceX API is currently unavailable.")
        print("Server of SpaceX images is currently unavailable. Try later.")

    collection = "spacecraft"
    try:
        fetch_hubble_images_by_collection(hubble_images_folder, collection=collection)
    except requests.HTTPError:
        logging.error(f"Hubble API is currently unavailable. Or couldn't find {collection} collection")
        print(f"Hubble API is currently unavailable or Impossible to find images in {collection} collection. "
              f"Check the spelling.")

    reformat_images_instagram_format(folders_to_get_images=[hubble_images_folder, spacex_images_folder],
                                     folder_to_save=insta_images_folder)

    username = os.environ["INSTAGRAM_USERNAME"]
    password = os.environ["INSTAGRAM_PASSWORD"]
    try:
        post_images_on_instagram(username, password, imgs_folder=insta_images_folder)
    except KeyError:
        print("Unable to find user or server is unavailable at the moment. Try later.")
