import os

from dotenv import load_dotenv
from instabot import Bot

from utils import find_all_images_in_folder


def post_images_on_instagram() -> None:
    """Posts images on instagram given their links.
    """

    print("Posting images on Instagram")
    bot = Bot()
    try:
        bot.login(username=os.environ['INSTAGRAM_USERNAME'], password=os.environ['INSTAGRAM_PASSWORD'])
    except KeyError:
        print("Service is temporarily unavailable. Try later.")
        return

    images_paths = find_all_images_in_folder('images/spacex/') + find_all_images_in_folder('images/hubble/')
    for image_path in images_paths:
        bot.upload_photo(image_path)


if __name__ == '__main__':
    load_dotenv()
    post_images_on_instagram()
