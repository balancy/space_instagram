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

    need_to_resize = any([size > MAX_DIMENSION for size in image.size])
    if need_to_resize:
        image.thumbnail((MAX_DIMENSION, MAX_DIMENSION))

    return image


def reformat_all_images_instagram_format(folders_to_get_images=None,
                                         folder_to_save="images/instagram/") -> None:
    """Reformat all images to instagram format and saves them in .jpg format.

    :param folders_to_get_images: folders where to get images paths
    :param folder_to_save: folder where to save reformatted images.
    """

    if not folders_to_get_images:
        images_paths = [*find_all_images_in_folder('images/spacex/'), *find_all_images_in_folder('images/hubble/')]
    else:
        images_paths = [image_path for folder in folders_to_get_images
                        for image_path in find_all_images_in_folder(folder)]

    for image_path in images_paths:
        filename_with_ext = os.path.split(image_path)[1]
        path_to_save = f"{folder_to_save}{filename_with_ext.split('.')[0]}.jpg"

        if not os.path.exists(path_to_save):
            image = resize_image(image_path)
            image.save(path_to_save, format='JPEG')


if __name__ == '__main__':
    reformat_all_images_instagram_format()
