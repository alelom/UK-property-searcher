import sys
import fnmatch
import os
import glob
import requests
import logging
import time

_logger = logging.getLogger()


def try_create_directory(path: str):
    try:
        os.makedirs(path)
        return True
    except BaseException as e:
        _logger.debug(e)

    return False


def get_logger():
    global _logger

    currentDateTime = time.strftime("%Y%m%d-%H%M%S")
    logger = logging.getLogger(currentDateTime)
    logger.setLevel(logging.DEBUG)
    try_create_directory("./_logs")

    log_file_path = rf'./_logs/{currentDateTime}.txt'
    fileHandler = logging.FileHandler(log_file_path)
    logFormatter = logging.Formatter("%(asctime)s | [%(levelname)s] %(message)s")
    fileHandler.setFormatter(logFormatter)
    logger.addHandler(fileHandler)

    streamHandler = logging.StreamHandler(stream=sys.stdout)
    streamHandler.setFormatter(logFormatter)
    logger.addHandler(streamHandler)

    _logger = logger

    logger.debug(f"Log created: {log_file_path}")
    return logger


def save_list_to_file(input_list: list, filepath: str = 'test.txt'):
    all_items_str = [str(item) for item in input_list]
    return save_text_list_to_file(all_items_str, filepath)


def save_text_list_to_file(input_list: list[str], filepath: str = 'test.txt'):
    with open(filepath, mode='wt', encoding='utf-8') as myfile:
        myfile.write('\n'.join(input_list))


def only_text_containing(texts: list, filter_texts: list, to_lower=False):
    result = set()
    for text in texts:
        for filter_text in filter_texts:
            if (to_lower and filter_text.lower() in text.lower()) or (filter_text in text):
                result.add(text)
    return list(result)


def exclude_text_containing(texts: list, filter_texts: list):
    to_exclude = only_text_containing(texts, filter_texts)
    return [t for t in texts if not t in to_exclude]


def floorplan_image_urls(texts: list):
    endings_to_exclude = ["_bp_pd_h_r.jpg", "_bp_mpu_r"]

    return exclude_text_containing(texts, endings_to_exclude)


def find_files(patterns: list[str], path):
    result = set()
    for root, dirs, files in os.walk(path):
        for name in files:
            for pattern in patterns:
                if fnmatch.fnmatch(name, pattern):
                    result.add(os.path.join(root, name))
    return list(result)


def ordinal(n: int):
    suffix = {1: 'st', 2: 'nd', 3: 'rd', 11: 'th', 12: 'th', 13: 'th'}
    return str(n) + (suffix.get(n % 100) or suffix.get(n % 10, 'th'))


def get_file_extension(file_path: str, include_dot: bool = True):
    if '.' not in file_path:
        _logger.debug(f"No extension found for file_path `{file_path}`")
        return ""
    extension = file_path.split(".")[-1]
    if include_dot:
        return "." + extension
    else:
        return extension


def file_exists_with_or_without_extension(filename):
    if glob.glob(filename):
        return True

    filename_no_extension = filename.split(".")[0]
    if glob.glob(filename_no_extension):
        return True

    return False


def download_image(pic_url: str, destination_file_path: str):
    """
    Downloads an image from an url and saves it where specified.
    :param pic_url: The url of the image.
    :param destination_file_path: The destination file path
    :return: True if successful.
    """
    try:
        with open(destination_file_path, 'wb') as handle:
            response = requests.get(pic_url, stream=True)

            if not response.ok:
                _logger.debug(response)
                return False

            for block in response.iter_content(1024):
                if not block:
                    break

                handle.write(block)

            return True
    except BaseException as e:
        _logger.debug(e)
        return False
