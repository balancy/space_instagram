from dotenv import load_dotenv
import requests

from fetch_hubble_images import fetch_hubble_images_by_collection
from fetch_spacex_images import fetch_spacex_last_launch_images
from post_instagram import post_images_on_instagram
from resize_images import resize_images_save_in_instagram_format


if __name__ == '__main__':
    requests.packages.urllib3.disable_warnings()
    load_dotenv()

    fetch_spacex_last_launch_images()
    fetch_hubble_images_by_collection('spacecraft')
    resize_images_save_in_instagram_format()
    post_images_on_instagram()
