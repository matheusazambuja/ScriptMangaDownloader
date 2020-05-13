from os.path import dirname, realpath
from ast import literal_eval
from manga import run_script
import yaml


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


def main():
    config = {}
    with open('config_download.yaml', 'r') as yaml_file:
        try:
            config = yaml.safe_load(yaml_file)
        except yaml.YAMLError as e:
            print(e)

    if config['manga_name'] == '':
        print(help(0))
    elif config['manga_chapters'] == '(,)' \
            or len(literal_eval(config['manga_chapters'])) != 2 \
            or not all(isinstance(item, int)
                       for item in literal_eval(config['manga_chapters'])):
        print(help(1))
    elif config['manga_path'] == '':
        print(help(2))
        input("Press Enter to continue...")
        config['manga_path'] = dirname(realpath(__file__))
        run_script(config['manga_name'], literal_eval(
            config['manga_chapters']), config['manga_path'])
    else:
        run_script(config['manga_name'], literal_eval(
            config['manga_chapters']), config['manga_path'])


if __name__ == '__main__':
    main()
