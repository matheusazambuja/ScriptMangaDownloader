import requests
import yaml
from os.path import dirname, realpath
from ast import literal_eval
from PIL import Image
from io import BytesIO
from manga import Manga, MangaDownload


HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1)' +
    'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


def config_chapters(manga_chapters):
    if manga_chapters.lower() == 'all':
        return (-1, -1)
    elif manga_chapters == '' \
        or len(literal_eval(manga_chapters)) != 2 \
        or not all(isinstance(item, int)
                   for item in literal_eval(manga_chapters)):
        print(help(1))
        exit(0)
    else:
        return literal_eval(manga_chapters)


def config_name(manga_name):
    if manga_name == '':
        print(help(0))
        exit(0)


def config_path(path):
    if path == '':
        print(help(2))
        if user_input() == 'y':
            path = dirname(realpath(__file__))
        else:
            exit(0)


def converting_image(bin_image, manga_dir):
    imgBytesIO = BytesIO(bin_image)
    img = Image.open(imgBytesIO)
    new_img = img.convert('RGB')
    new_img.save(manga_dir.replace('.webp', '.jpg'), 'jpeg', quality=100)


def get_configs():
    with open('config_download.yaml', 'r') as yaml_file:
        try:
            config = yaml.safe_load(yaml_file)
            return config
        except yaml.YAMLError as e:
            print(e)


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


def request(link):
    try:
        return requests.get(link, headers=HEADERS)
    except requests.exceptions.RequestException as e:
        print(e)


def run_script(name, chapters, path, domain):
    manga = MangaDownload(name)
    MangaRight = Manga(manga.name, manga.link, chapters, path)
    MangaRight.download_chapters()


def user_input():
    while True:
        choice = input("Do you wish to continue (Y/N)?")
        if choice.lower() in ('y', 'n'):
            break
    return choice.lower()
