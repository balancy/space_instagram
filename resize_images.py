import os

from PIL import Image

from utils import find_all_images_in_folder

MAX_DIMENSION = 1080


def resize_image(image_path):
    """Resizes image to instagram format.

    :param image_path: path to the image
    :return: resized image
    """

    image = Image.open(image_path)
    if image.mode != 'RGB':
        image = image.convert("RGB")

    width, height = image.size

    max_dimension_instagram = MAX_DIMENSION
    max_dimension_image = max([width, height])
    coefficient_reduce = max_dimension_image / max_dimension_instagram \
        if max_dimension_image > max_dimension_instagram else 1

    if coefficient_reduce > 1:
        image.thumbnail((int(width / coefficient_reduce), int(height / coefficient_reduce)))

    return image


def reformat_all_images_instagram_format() -> None:
    """Reformat all images to instagram format and saves them in .jpg format.
    """

    folder_to_save = "images/instagram/"
    os.makedirs(folder_to_save, exist_ok=True)

    images_paths = find_all_images_in_folder('images/spacex/') + find_all_images_in_folder('images/hubble/')
    for image_path in images_paths:
        filename_with_ext = os.path.split(image_path)[1]
        path_to_save = f"{folder_to_save}{filename_with_ext.split('.')[0]}.jpg"

        if not os.path.exists(path_to_save):
            image = resize_image(image_path)
            image.save(path_to_save, format='JPEG')


if __name__ == '__main__':
    reformat_all_images_instagram_format()
