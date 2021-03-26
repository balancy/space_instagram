import os


def find_all_images_in_folder(folder='images/'):
    """Finds all images in given folder and its subfolders.

    :param folder: folder to search files inside
    :return: files in folder and its subfolders
    """

    files_paths = []
    for dirpath, _, filenames in os.walk(folder):
        for filename in filenames:
            files_paths.append(os.path.join(dirpath, filename))

    return files_paths


if __name__ == '__main__':
    paths = find_all_images_in_folder()
