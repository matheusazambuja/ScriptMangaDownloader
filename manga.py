import requests
import os
import errno


class Manga:
    def __init__(self, name, chapters, path, domain):
        self.name = name
        self.chapters = []
        self._create_chapters(chapters, path, domain)
        self.path = path
        self.domain = domain

    def _create_chapters(self, chapters, path, domain):
        for i in range(chapters[0], chapters[-1]+1):
            if i in range(0, 10):
                self.chapters.append(Chapter(self.name, chr(
                    ord('0')) + str(i), path, domain))
            else:
                self.chapters.append(
                    Chapter(self.name, str(i), path, domain))

    def download_chapters(self):
        for chapter in self.chapters:
            chapter.download_pages()


class Chapter():
    def __init__(self, name, number, path, domain):
        self.name = name
        self.number = number
        self.links_pages = []
        self.path = path
        self.domain = domain

    def _change_page(self, old_page):
        if len(self.links_pages) % 10 == 0:
            new_page = chr(ord(old_page[0]) + 1) + '0'
        else:
            new_page = old_page[0] + chr(ord(old_page[-1]) + 1)
        return ['https://' + self.domain +
                '/mangas/' + self.name + '/capitulo-' +
                str(self.number) + '/' + new_page + '.jpg', new_page]

    def _set_dir_pages(self, number_page):
        manga_dir = self.path + '\\' + self.name + '\\' + \
            str(self.number) + '\\' + str(number_page) + '.jpg'

        if not os.path.exists(os.path.dirname(manga_dir)):
            try:
                os.makedirs(os.path.dirname(manga_dir))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        return manga_dir

    def get_links_pages(self):
        self.links_pages = []
        new_page = '00'
        url = 'https://' + self.domain + '/mangas/' + self.name + \
            '/capitulo-' + str(self.number) + '/' + new_page + '.jpg'
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
        self.get_links_pages()

        print('Download started')
        for i_page, page in enumerate(self.links_pages):
            print(f'Page number: {i_page}')
            r = requests.get(page)

            manga_dir = self._set_dir_pages(i_page)

            with open(manga_dir, 'wb') as image:
                image.write(r.content)
            r = requests.get(page)
        print('Download completed')
