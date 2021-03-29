import os

from dotenv import load_dotenv
from instabot import Bot

from utils import find_all_images_in_folder


def post_images_on_instagram(username, password, imgs_folder="images/instagram/") -> None:
    """Posts images on instagram given their links.

    :param username; instagram username
    :param password: instagram password
    :param imgs_folder: path where to get photos to upload to instagram
    """

    bot = Bot()
    bot.login(username=username, password=password)

    images_paths = find_all_images_in_folder(imgs_folder)
    for image_path in images_paths:
        bot.upload_photo(image_path)


if __name__ == "__main__":
    load_dotenv()

    username = os.environ["INSTAGRAM_USERNAME"]
    password = os.environ["INSTAGRAM_PASSWORD"]
    post_images_on_instagram(username, password)
