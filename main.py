import utils


def main():
    config = utils.get_configs()
    if not config['error']:
        params = config['return']
        utils.run_script(params['manga_name'], params['manga_chapters'], params['manga_path'])
    else:
        [print(e) for e in config['error']]


if __name__ == '__main__':
    main()
