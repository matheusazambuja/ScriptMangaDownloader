from os.path import dirname, realpath
from ast import literal_eval
from manga import run_script
import yaml
import utils


def main():
    config = {}
    with open('config_download.yaml', 'r') as yaml_file:
        try:
            config = yaml.safe_load(yaml_file)
        except yaml.YAMLError as e:
            print(e)

    if config['manga_name'] == '':
        print(utils.help(0))
    elif config['manga_chapters'] == '(,)' \
            or len(literal_eval(config['manga_chapters'])) != 2 \
            or not all(isinstance(item, int)
                       for item in literal_eval(config['manga_chapters'])):
        print(utils.help(1))
    elif config['manga_path'] == '':
        print(utils.help(2))
        input("Press Enter to continue...")
        config['manga_path'] = dirname(realpath(__file__))
        run_script(config['manga_name'], literal_eval(
            config['manga_chapters']), config['manga_path'])
    else:
        run_script(config['manga_name'], literal_eval(
            config['manga_chapters']), config['manga_path'])


if __name__ == '__main__':
    main()
