import requests
from os.path import dirname, realpath

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1)' +
    'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


def request(link):
    try:
        return requests.get(link, headers=HEADERS)
    except requests.exceptions.RequestException as e:
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
