import utils


def main():
    params = utils.get_configs()

    utils.config_name(params['manga_name'])
    params['manga_chapters'] = utils.config_chapters(params['manga_chapters'])
    utils.config_path(params['manga_path'])

    utils.run_script(params['manga_name'], params['manga_chapters'],
                     params['manga_path'], params['manga_domain'])


if __name__ == '__main__':
    main()
