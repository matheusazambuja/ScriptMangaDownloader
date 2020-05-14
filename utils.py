import requests
from os.path import dirname, realpath
from PIL import Image
from io import BytesIO

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1)' +
    'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


def request(link):
    try:
        return requests.get(link, headers=HEADERS)
    except requests.exceptions.RequestException as e:
        print(e)


def converting_image(bin_image, manga_dir):
    imgBytesIO = BytesIO(bin_image)
    img = Image.open(imgBytesIO)
    new_img = img.convert('RGB')
    new_img.save(manga_dir.replace('.webp', '.jpg'), 'jpeg', quality=100)


def help(code):
    ERRORS_CODE = {
        0: """
    In config_download.yaml:
    Name manga not defined.
    Parameter: <manga_name>
    Example: tower-of-god-season-1 - Name manga for download""",
        1: """
    In config_download.yaml:
    Parameter: <manga_chapters> error defined
    Example: (1,3) - Chapters manga 1 to 3 for download""",
        2: """
    In config_download.yaml:
    Parameter: <manga_path> is empty
    Example: C:/Users/You/Documents
    So, standart directory seted will script path {}
    """.format(dirname(realpath(__file__)))}
    return ERRORS_CODE.get(code)
