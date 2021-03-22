import os


def find_all_images_in_folder(folder='images/'):
    """

    :param folder:
    :return: files in folder and its subfolders
    """

    files_paths = []
    for dirpath, _, filenames in os.walk(folder):
        for filename in [f for f in filenames]:
            files_paths.append(os.path.join(dirpath, filename))

    return files_paths
