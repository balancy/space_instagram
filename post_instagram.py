import os

from dotenv import load_dotenv
from instabot import Bot

from utils import find_all_images_in_folder


def post_images_on_instagram(path_images="images/instagram/") -> None:
    """Posts images on instagram given their links.

    :param path_images: path where to get photos to upload to instagram
    """

    bot = Bot()
    bot.login(username=os.environ['INSTAGRAM_USERNAME'], password=os.environ['INSTAGRAM_PASSWORD'])

    images_paths = find_all_images_in_folder(path_images)
    for image_path in images_paths:
        bot.upload_photo(image_path)


if __name__ == '__main__':
    load_dotenv()
    post_images_on_instagram()
