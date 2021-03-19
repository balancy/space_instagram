import os

import requests

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


def fetch_images_from_urls(images_urls, folder='images/spacex/') -> None:
    """Download images from urls given in a list.

    :param images_urls: list of images urls
    :param folder: folder to save images
    """

    print("Downloading SpaceX last launch images:")

    check_folder(folder)

    for image_url in images_urls:
        r = requests.get(image_url)
        r.raise_for_status()

        physical_path_to_photo = f"{folder}{image_url.split('/')[-1]}"
        with open(physical_path_to_photo, 'wb') as image:
            image.write(r.content)

    print("Downloading SpaceX images finished")


def find_hubble_images_ids_by_collection(collection='spacecraft') -> list:
    """Finds ids of hubble images by collection.

    :param collection: collection of images to search
    :return: list of images ids
    """

    r = requests.get(f"{HUBBLE_API_URL}s", params={'collection_name': collection})
    r.raise_for_status()

    return [elm.get('id') for elm in r.json()]


def fetch_hubble_images_by_ids(images_ids, folder='images/hubble/') -> None:
    """Finds hubble best quality images bu ids and download them.

    :param images_ids: ids of the images
    :param folder: folder to save images
    """

    print("Downloading Hubble images:")

    check_folder(folder)

    for image_id in images_ids:
        print(f"- image with id {image_id} is downloading")

        r = requests.get(f"{HUBBLE_API_URL}/{image_id}", verify=False)
        r.raise_for_status()

        image_url = f"https:{r.json().get('image_files')[-1].get('file_url')}"
        r = requests.get(image_url, verify=False)
        r.raise_for_status()

        physical_path_to_photo = f"{folder}{image_id}.{image_url.split('.')[-1]}"
        with open(physical_path_to_photo, 'wb') as image:
            image.write(r.content)

        print(f"+ image finished downloading")

    print("Downloading Hubble images finished")


if __name__ == '__main__':
    requests.packages.urllib3.disable_warnings()

    try:
        # spacex images
        spacex_images_urls = find_spacex_last_launch_images_urls()
        fetch_images_from_urls(spacex_images_urls)

        # hubble images
        hubble_images_ids = find_hubble_images_ids_by_collection()
        fetch_hubble_images_by_ids(hubble_images_ids)
    except requests.HTTPError as e:
        print(e)
