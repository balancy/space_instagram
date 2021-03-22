import os

from PIL import Image

from utils import find_all_images_in_folder


def resize_images_save_in_instagram_format() -> None:
    """Resizes images to have a 1080px as maximum dimension and saves them in .jpg format.
    """

    folder_to_save = "images/instagram/"
    os.makedirs(folder_to_save, exist_ok=True)

    images_paths = find_all_images_in_folder('images/spacex/') + find_all_images_in_folder('images/hubble/')
    for image_path in images_paths:
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


if __name__ == '__main__':
    resize_images_save_in_instagram_format()
