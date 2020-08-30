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
        return {
            'error': None,
            'function': 'config_chapters',
            'return': (-1, -1)}
    elif manga_chapters == '' or len(literal_eval(manga_chapters)) != 2 or not all(isinstance(item, int)
                   for item in literal_eval(manga_chapters)):
        return {
            'error': help(1),
            'function': 'config_chapters',
            'return': None}
    else:
        return {
            'error': None,
            'function': 'config_chapters',
            'return': literal_eval(manga_chapters)}


def config_name(manga_name):
    if manga_name == '':
        return {
            'error': help(0),
            'function': 'config_name',
            'return': None}
    else:
        return {
            'error': None,
            'function': 'config_name',
            'return': True}


def config_path(path):
    if path == '':
        print(help(2))
        if user_input() == 'y':
            path = dirname(realpath(__file__))
            return {
                'error': None,
                'function': 'config_path',
                'return': None}
        else:
            return {
                'error': 'standart directory seted will script path',
                'function': 'config_path',
                'return': None}
    else:
        return {
            'error': None,
            'function': 'config_path',
            'return': None}


def converting_image(bin_image, manga_dir):
    imgBytesIO = BytesIO(bin_image)
    img = Image.open(imgBytesIO)
    new_img = img.convert('RGB')
    new_img.save(manga_dir.replace('.webp', '.jpg'), 'jpeg', quality=100)


def get_configs():
    with open('config_download.yaml', 'r') as yaml_file:
        try:
            config = yaml.safe_load(yaml_file)
            list_errors = []

            test_name = config_name(config['manga_name'])
            if test_name['error']:
                list_errors.append(test_name['error'])

            test_chapters = config_chapters(config['manga_chapters'])
            if test_chapters['error']:
                list_errors.append(test_chapters['error'])
            else:
                config['manga_chapters'] = literal_eval(config['manga_chapters'])

            test_path = config_path(config['manga_path'])
            if test_path['error']:
                list_errors.append(test_path['error'])

            if not list_errors:
                return {
                    'error': None,
                    'function': 'get_configs',
                    'return': config}
            else:
                return {
                    'error': list_errors,
                    'function': 'get_configs',
                    'return': None}
        except yaml.YAMLError as e:
            return {
                'error': e,
                'function': 'get_configs',
                'return': None}
                

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


def run_script(name, chapters, path):
    manga = MangaDownload(name)
    MangaRight = Manga(manga.name, manga.link, chapters, path)
    MangaRight.download_chapters()


def user_input():
    while True:
        choice = input("Do you wish to continue (Y/N)?")
        if choice.lower() in ('y', 'n'):
            break
    return choice.lower()

def _radix_sort_msd(lista, i):
    if len(lista) <= 1:
        return lista
    else:
        lista_ordenada = []
        lista_aux = [[] for x in range(36)]  # 37: um espaço para cada letra do alfabeto e numeros

        for s in lista:
            if i >= len(s):
                lista_ordenada.append(s)
            else:
                if s[i].isdigit():
                    lista_aux[ord(s[i]) - 48].append(s)
                else:
                    lista_aux[ord(s[i].upper()) - ord('A') + 10].append(s)

        lista_aux = [_radix_sort_msd(b, i + 1) for b in lista_aux]

        return lista_ordenada + [b for blist in lista_aux for b in blist]

def _clear_string(string, alphabet):
    i = 0
    cleaned_string = string
    while i < len(cleaned_string):
        if cleaned_string[i].upper() not in alphabet:
            cleaned_string = cleaned_string.replace(cleaned_string[i], '')
        else:
            i += 1
    return cleaned_string

def sort_mangas(list_mangas, query):
    alphabet = [chr(c) for c in range(48, 58)] + [chr(c) for c in range(65, 91)]
    nameclean_and_manga = [[_clear_string(a['title'], alphabet), a] for a in list_mangas]

    mangas = []
    query = _clear_string(query, alphabet).upper()
    for element in nameclean_and_manga:
        dif = False
        i, j = 0, 0
        index = min(len(query), len(element[0]))
        element[0] = element[0].upper()
        while i < len(query) and j < len(element[0]):
            if query[i] != element[0][j]:
                if element[0][j-1] != element[0][j]:
                    dif = True
                    break
                else:
                    j += 1
            else:
                j += 1
                i += 1
        if not dif and i >= len(query):
            mangas.append(element)
    mangas_sorted = []
    names_sort = _radix_sort_msd([a[0] for a in mangas], 0)
    for i, n in enumerate(names_sort):
        for a in mangas:
            if n == a[0]:
                mangas_sorted.append(a[-1])
                break

    return mangas_sorted