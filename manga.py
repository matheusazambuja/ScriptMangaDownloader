import os
import errno
import re
import utils
from collections import OrderedDict
from bs4 import BeautifulSoup


class MangaDownload:
    def __init__(self, name):
        self.name = name
        self.link = ''
        self._select_manga()

    def find_manga_html(self):
        mangas = []
        b_html = utils.request('https://mangahost.site/find/' +
                               self.name.replace(' ', '+'))
        soup = BeautifulSoup(b_html.content, 'html.parser')
        for tag in soup.find_all('h3', class_='entry-title'):
            tag = tag.find('a')
            tag = str(tag).replace('"', "'")
            link = re.findall(r"(?<=<a href=')[^']*", str(tag))
            name = re.findall(r"(?<=title=')[^']*", str(tag))
            mangas.append([name[0], link[0]])
        return mangas

    def _select_manga(self):
        mangas = self.find_manga_html()
        print('-----------------------------------------------')
        print('Enter 0 to end execution.')
        print('-----------------------------------------------')
        print(f'Found mangas:')
        for manga in mangas:
            print(f'{mangas.index(manga)+1}: {manga[0]}')
        code_manga = 'a'
        while not code_manga.isdigit() \
                or int(code_manga)-1 not in range(len(mangas)):
            code_manga = input(f'Select a manga: ')
            if code_manga == '0':
                exit(0)
        self.name = mangas[int(code_manga)-1][0]
        self.link = mangas[int(code_manga)-1][1]


class Manga:
    def __init__(self, name, link, chapters, path):
        self.name = name
        self.link = link
        self.chapters = chapters
        self.path = path

    def find_chapters_html(self):
        links_chapters = []
        b_html = utils.request(self.link)
        soup = BeautifulSoup(b_html.content, 'html.parser')

        id_manga = re.search(r'mh\d+', b_html.url)
        regex_links_chapters = r"\bhref=['\"](\S+" + \
            re.escape(id_manga.group(0)) + r"\S+)\b"
        links_chapters = re.findall(regex_links_chapters, str(soup))
        links_chapters = list(OrderedDict.fromkeys(links_chapters))

        chapters_return = []
        links_chapters.reverse()
        if self.chapters == (-1, -1):
            find_first_manga = True
        else:
            find_first_manga = False
        for link in links_chapters:
            regex_id_chapter = re.escape(
                id_manga.group(0)) + r'/(\w+(.\w+)?)'
            id_chapter = re.search(regex_id_chapter, link)
            id_chapter = re.sub(
                re.escape(id_manga.group(0)) + r'/', '', id_chapter.group(0))
            if id_chapter.isdigit() and id_chapter == str(self.chapters[0]):
                find_first_manga = True
            if find_first_manga:
                chapters_return.append([id_chapter, link])
                if id_chapter.isdigit() and id_chapter == str(self.chapters[1]):
                    break
        return chapters_return

    def download_chapters(self):
        chapters_num = self.find_chapters_html()
        for chapter in chapters_num:
            print(chapter[0], chapter[1])
            Chapter(self.name, chapter[0], chapter[1],
                    self.path).download_pages()


class Chapter():
    def __init__(self, name, id_chapter, link, path):
        self.name = name
        self.id_chapter = id_chapter
        self.link = link
        self.path = path

    def save_page(self, number_page, bin_image):
        manga_dir = self.path + '\\' + self.name + '\\' + \
            str(self.id_chapter) + '\\' + str(number_page) + '.webp'

        if not os.path.exists(os.path.dirname(manga_dir)):
            try:
                os.makedirs(os.path.dirname(manga_dir))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        utils.converting_image(bin_image, manga_dir)

    def find_pages_html(self):
        pages = []
        b_html = utils.request(self.link)
        soup = BeautifulSoup(b_html.content, 'html.parser')
        regex_pages = r"\bsrc='(\w+://[\w.%+-/ ]+)"
        for tag in soup.find_all('script'):
            pages = re.findall(regex_pages, str(tag))
            if pages:
                return pages

    def download_pages(self):
        print('-----------------------------------------------')
        print(f'{self.name} - Chapter: {self.id_chapter}')
        links_pages = self.find_pages_html()
        total_pages_download = 1
        if links_pages:
            print('Download started')
            for link in links_pages:
                r = utils.request(link)
                self.save_page(total_pages_download, r.content)
                total_pages_download += 1
            print('Download completed')
            print(f'Total pages download: {total_pages_download}')
            print('-----------------------------------------------')
        else:
            print(f'Pages not found')
            print('-----------------------------------------------')
