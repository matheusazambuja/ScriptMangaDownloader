from os.path import dirname, realpath
from ast import literal_eval
from manga import Manga
import yaml

# Domain of sites for downloads:
DOMAIN = {'GOYABU': 'mangayabu.com'}


def help(code):
    ERRORS_CODE = {
        0: """
In config_download.json:
Name manga not defined.
Parameter: <manga_name>
Example: tower-of-god-season-1 - Name manga for download""",
        1: """
In config_download.json:
Parameter: <manga_chapters> error defined
Example: (1, 3) - Chapters manga 1 to 3 for download""",
        2: """
In config_download.json:
Parameter: <manga_domain> is empty
Example: mangayabu.com - Site used to do download""",
        3: """
In config_download.json:
Parameter: <manga_path> is empty
So, standart directory seted will script path {}
Example: C:/Users/You/Documents
""".format(dirname(realpath(__file__)))}
    return ERRORS_CODE.get(code)


def main():
    datas = {}
    with open('config_download.yaml', 'r') as yaml_file:
        try:
            datas = yaml.safe_load(yaml_file)
        except yaml.YAMLError as e:
            print(e)

    if datas['manga_name'] == '':
        print(help(0))
    elif datas['manga_chapters'] == '(,)' \
            or len(literal_eval(datas['manga_chapters'])) != 2 \
            or not all(isinstance(item, int)
                       for item in literal_eval(datas['manga_chapters'])):
        print(help(1))
    elif datas['manga_domain'] == '':
        print(help(2))
    elif datas['manga_path'] == '':
        print(help(3))
        input("Press Enter to continue...")
        datas['manga_path'] = dirname(realpath(__file__))
        manga = Manga(datas['manga_name'],
                      literal_eval(datas['manga_chapters']),
                      datas['manga_domain'], datas['manga_path'])
        manga.download_chapters()
    else:
        manga = Manga(datas['manga_name'],
                      literal_eval(datas['manga_chapters']),
                      datas['manga_domain'], datas['manga_path'])
        manga.download_chapters()


if __name__ == '__main__':
    main()
