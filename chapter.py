import requests
import os
import errno
from manga import Manga


class Chapter(Manga):
    def __init__(self, name, number):
        self.name = name
        self.number = number
        self.links_pages = []
        self.url_pattern = ''
        self._create_url_pattern()

    def _create_url_pattern(self):
        self.url_pattern = 'https://' + \
            DOMAIN['GOYABU'] + '/mangas/' + self.name + \
            '/capitulo-' + str(self.number) + '/00.jpg'

    def _change_page(self, old_page):
        if len(self.links_pages) % 10 == 0:
            new_page = chr(ord(old_page[0]) + 1) + '0'
        else:
            new_page = old_page[0] + chr(ord(old_page[-1]) + 1)
        return ['https://' + DOMAIN['GOYABU'] + '/mangas/' + self.name +
                '/capitulo-' + str(self.number) + '/' + new_page + '.jpg', new_page]

    # def _log_get_links_pages(self, function):
    #     def decorator(*args, **kwargs):
    #         print(f'Getting pages links of manga:')
    #         print(f'Manga: {self.name} - Chapter: {self.number}')
    #         function(*args, **kwargs)
    #         print(f'Getting completed')
    #     return decorator

    # @_log_get_links_pages
    def get_links_pages(self, url):
        self.links_pages = []
        new_page = '00'
        r = requests.get(url)

        print(f'Getting pages links of manga:')

        while r.url != 'https://mangayabu.com/?error=404':
            self.links_pages.append(r.url)

            old_page = new_page
            [url, new_page] = self._change_page(old_page)
            print(f'Page link: {url}')
            r = requests.get(url)
        print(f'Getting completed')

    def download_pages(self):
        print(f'Manga: {self.name} - Chapter: {self.number}')
        self.get_links_pages(self.url_pattern)

        print('Download started')
        for i_link, link in enumerate(self.links_pages):
            filename = 'D:/Files/matheus/faculdade/tests/test_downloader/' + \
                self.name + '/' + str(self.number) + '/' + str(i_link) + '.jpg'

            if not os.path.exists(os.path.dirname(filename)):
                try:
                    os.makedirs(os.path.dirname(filename))
                except OSError as exc:  # Guard against race condition
                    if exc.errno != errno.EEXIST:
                        raise
            print(f'Page number: {i_link}')
            r = requests.get(link)
            with open(filename, 'wb') as image:
                image.write(r.content)
            r = requests.get(link)
        print('Download completed')
