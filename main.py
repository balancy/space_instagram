import os

from instabot import Bot
from PIL import Image
import requests

from settings import USERNAME, PASSWORD

SPACEX_API_URL = "https://api.spacexdata.com/v3/launches"
HUBBLE_API_URL = "http://hubblesite.org/api/v3/image"


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


def fetch_spacex_last_launch_images() -> list:
    """Download SpaceX last launch images.

    :return: physical paths to images
    """

    print("Searching for SpaceX last launch images on web")
    try:
        images_urls = find_spacex_last_launch_images_urls()
    except requests.HTTPError:
        return []

    print("Downloading SpaceX last launch images")
    folder = 'images/spacex/'
    check_folder(folder)

    paths_to_images = []
    for image_url in images_urls:
        physical_path_to_photo = f"{folder}{image_url.split('/')[-1]}"

        if not os.path.exists(physical_path_to_photo):
            r = requests.get(image_url)
            try:
                r.raise_for_status()
            except requests.HTTPError:
                continue

            with open(physical_path_to_photo, 'wb') as image:
                image.write(r.content)

        paths_to_images.append(physical_path_to_photo)

    print("Downloading finished")
    return paths_to_images


def find_hubble_images_ids_by_collection(collection='spacecraft') -> list:
    """Finds ids of hubble images by collection.

    :param collection: collection of images to search
    :return: list of images ids
    """

    r = requests.get(f"{HUBBLE_API_URL}s", params={'collection_name': collection})
    try:
        r.raise_for_status()
    except requests.HTTPError:
        print(f"Impossible to find hubble images in {collection} collection")
        return []

    return [elm.get('id') for elm in r.json()]


def fetch_hubble_images_by_collection(collection='spacecraft') -> list:
    """Downloads hubble best quality images bu collection.

    :param collection: collection of images to search
    :return: physical paths to images
    """

    print(f"Searching for Hubble images ids in '{collection}' collection")
    images_ids = find_hubble_images_ids_by_collection(collection)
    if not images_ids:
        return []

    print(f"Downloading Hubble images in '{collection}' collection")
    folder = 'images/hubble/'
    check_folder(folder)

    path_to_images = []
    for image_id in images_ids:
        print(f"- image with id {image_id} is checking")

        r = requests.get(f"{HUBBLE_API_URL}/{image_id}", verify=False)
        try:
            r.raise_for_status()
        except requests.HTTPError:
            continue

        image_url = f"https:{r.json().get('image_files')[-1].get('file_url')}"
        physical_path_to_photo = f"{folder}{image_id}.{image_url.split('.')[-1]}"

        if not os.path.exists(physical_path_to_photo):
            print(f"- image with id {image_id} is downloading")
            r = requests.get(image_url, verify=False)
            try:
                r.raise_for_status()
            except requests.HTTPError:
                continue

            with open(physical_path_to_photo, 'wb') as image:
                image.write(r.content)

        path_to_images.append(physical_path_to_photo)

    print("Downloading Hubble images finished")


def find_all_images_in_folder(folder='images/'):
    """

    :param folder:
    :return: files in folder and its subfolders
    """

    files_paths = []
    for dirpath, _, filenames in os.walk(folder):
        # for filename in [f for f in filenames if f.endswith(".jpg")]:
        for filename in [f for f in filenames]:
            files_paths.append(os.path.join(dirpath, filename))

    return files_paths


def resize_save_images_instagram_format() -> None:
    """Resizes images to have a 1080px as maximum dimension and saves it in .jpg format.
    """

    print("Resizing images:")
    folder_to_save = "images/instagram/"
    check_folder(folder_to_save)

    images_paths = find_all_images_in_folder('images/spacex/') + find_all_images_in_folder('images/hubble/')
    for image_path in images_paths:
        print(f"- processing image '{image_path}'")
        filename = image_path.split('/')[-1]
        path_to_save = f"{folder_to_save}{filename.split('.')[0]}.jpg"

        if not os.path.exists(path_to_save):
            image = Image.open(image_path)
            if image.mode != 'RGB':
                image = image.convert("RGB")

            width, height = image.size

            max_dimension_instagram = 1080
            max_dimension_image = max([width, height])
            coefficient_reduce = max_dimension_image/max_dimension_instagram \
                if max_dimension_image > max_dimension_instagram else 1

            if coefficient_reduce > 1:
                image.thumbnail((int(width/coefficient_reduce), int(height/coefficient_reduce)))
            image.save(path_to_save, format='JPEG')
            print(f"- image '{path_to_save}' is processed")

    print("Resizing is finished")


def post_images_instagram() -> None:
    """Posts images on instagram given their links.
    """

    bot = Bot()
    bot.login(username=USERNAME, password=PASSWORD)

    images_paths = find_all_images_in_folder('images/spacex/') + find_all_images_in_folder('images/hubble/')
    for image_path in images_paths:
        bot.upload_photo(image_path)


if __name__ == '__main__':
    requests.packages.urllib3.disable_warnings()

    spacex_images_paths = fetch_spacex_last_launch_images()
    hubble_images_paths = fetch_hubble_images_by_collection('spacecraft')
    resize_save_images_instagram_format()
    post_images_instagram()
