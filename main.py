import os

from dotenv import load_dotenv
import requests

from fetch_hubble_images import fetch_hubble_images_by_collection
from fetch_spacex_images import fetch_spacex_last_launch_images
from post_instagram import post_images_on_instagram
from resize_images import reformat_images_instagram_format


if __name__ == '__main__':
    requests.packages.urllib3.disable_warnings()
    load_dotenv()

    folder_hubble_images = "images/hubble/"
    folder_spacex_images = "images/spacex/"
    folder_insta_images = "images/instagram/"

    os.makedirs(folder_spacex_images, exist_ok=True)
    os.makedirs(folder_hubble_images, exist_ok=True)
    os.makedirs(folder_insta_images, exist_ok=True)

    fetch_spacex_last_launch_images(folder_spacex_images)
    fetch_hubble_images_by_collection(folder_hubble_images, collection='spacecraft')
    reformat_images_instagram_format(folders_to_get_images=[folder_hubble_images, folder_spacex_images],
                                     folder_to_save=folder_insta_images)
    post_images_on_instagram(path_images=folder_insta_images)
