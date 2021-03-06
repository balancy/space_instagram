import os

import requests

HUBBLE_API_URL = "http://hubblesite.org/api/v3/image"


def find_hubble_images_ids_by_collection(collection="spacecraft"):
    """Finds ids of hubble images by collection.

    :param collection: collection of images to search
    :return: list of images ids
    """

    response = requests.get(f"{HUBBLE_API_URL}s", params={"collection_name": collection})
    response.raise_for_status()

    return [elm.get("id") for elm in response.json()]


def fetch_hubble_images_by_collection(folder_to_save="images/hubble/", collection="spacecraft"):
    """Downloads hubble best quality images bu collection.

    :param folder_to_save: folder to save images
    :param collection: collection of images to search
    """

    images_ids = find_hubble_images_ids_by_collection(collection)

    for image_id in images_ids:
        response = requests.get(f"{HUBBLE_API_URL}/{image_id}", verify=False)
        response.raise_for_status()

        image_url = f"https:{response.json().get('image_files')[-1].get('file_url')}"
        physical_path_to_photo = f"{folder_to_save}{image_id}.{os.path.splitext(image_url)[1]}"

        if not os.path.exists(physical_path_to_photo):
            response = requests.get(image_url, verify=False)
            response.raise_for_status()

            with open(physical_path_to_photo, "wb") as image:
                image.write(response.content)


if __name__ == "__main__":
    fetch_hubble_images_by_collection()
