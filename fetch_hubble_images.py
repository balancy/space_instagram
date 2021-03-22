import os

import requests

from utils import check_folder

HUBBLE_API_URL = "http://hubblesite.org/api/v3/image"


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


def fetch_hubble_images_by_collection(collection='spacecraft') -> None:
    """Downloads hubble best quality images bu collection.

    :param collection: collection of images to search
    """

    images_ids = find_hubble_images_ids_by_collection(collection)
    if not images_ids:
        return []

    folder = 'images/hubble/'
    check_folder(folder)

    path_to_images = []
    for image_id in images_ids:
        r = requests.get(f"{HUBBLE_API_URL}/{image_id}", verify=False)
        try:
            r.raise_for_status()
        except requests.HTTPError:
            continue

        image_url = f"https:{r.json().get('image_files')[-1].get('file_url')}"
        physical_path_to_photo = f"{folder}{image_id}.{image_url.split('.')[-1]}"

        if not os.path.exists(physical_path_to_photo):
            r = requests.get(image_url, verify=False)
            try:
                r.raise_for_status()
            except requests.HTTPError:
                continue

            with open(physical_path_to_photo, 'wb') as image:
                image.write(r.content)

        path_to_images.append(physical_path_to_photo)


if __name__ == '__main__':
    fetch_hubble_images_by_collection()
