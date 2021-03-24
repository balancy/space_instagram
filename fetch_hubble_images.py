import os

import requests

HUBBLE_API_URL = "http://hubblesite.org/api/v3/image"


def find_hubble_images_ids_by_collection(collection='spacecraft'):
    """Finds ids of hubble images by collection.

    :param collection: collection of images to search
    :return: list of images ids
    """

    response = requests.get(f"{HUBBLE_API_URL}s", params={'collection_name': collection})
    response.raise_for_status()

    response_json_format = response.json()
    return [elm.get('id') for elm in response_json_format]


def fetch_hubble_images_by_collection(folder_to_save="images/hubble/", collection='spacecraft') -> None:
    """Downloads hubble best quality images bu collection.

    :param folder_to_save: folder to save images
    :param collection: collection of images to search
    """

    images_ids = find_hubble_images_ids_by_collection(collection)

    path_to_images = []
    for image_id in images_ids:
        response = requests.get(f"{HUBBLE_API_URL}/{image_id}", verify=False)
        if response.status_code == 404:
            continue

        image_url = f"https:{response.json().get('image_files')[-1].get('file_url')}"
        physical_path_to_photo = f"{folder_to_save}{image_id}.{image_url.split('.')[-1]}"

        if not os.path.exists(physical_path_to_photo):
            response = requests.get(image_url, verify=False)
            if response.status_code == 404:
                continue

            with open(physical_path_to_photo, 'wb') as image:
                image.write(response.content)

        path_to_images.append(physical_path_to_photo)


if __name__ == '__main__':
    fetch_hubble_images_by_collection()
