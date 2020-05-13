import requests
import os
import errno
import re
import utils
from bs4 import BeautifulSoup
from collections import OrderedDict

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


class MangaDownload:
    def __init__(self, name):
        self.name = name
        self.link = ''
        self.select_manga()

    def find_manga_html(self):
        b_html = utils.request('find/', self.name, '')
        if b_html is not None:
            mangas = []
            bs = BeautifulSoup(b_html.content, "lxml")
            for tag in bs.find_all('h3', class_='entry-title'):
                tag = tag.find('a')
                tag = str(tag).replace('"', "'")
                link = re.findall(r"(?<=<a href=')[^']*", str(tag))
                name = re.findall(r"(?<=title=')[^']*", str(tag))
                mangas.append([name[0], link[0]])
            return mangas
        else:
            return None

    def select_manga(self):
        mangas = self.find_manga_html()
        print(f'Found mangas:')
        for manga in mangas:
            print(f'{mangas.index(manga)}: {manga[0]}')
        code_manga = 'a'
        while not code_manga.isdigit() \
                or int(code_manga) not in range(len(mangas)):
            code_manga = input(f'Select a manga: ')
        self.name = mangas[int(code_manga)][0]
        self.link = mangas[int(code_manga)][1]


class Manga:
    def __init__(self, name, link, chapters, path):
        self.name = name
        self.link = link
        self.chapters = chapters
        self.path = path

    def find_chapters_html(self):
        b_html = utils.request('', '', self.link)
        if b_html:
            links_chapters = []
            soup = BeautifulSoup(b_html.content, "lxml")

            id_manga = re.search(r'mh\d+', b_html.url)
            regex_links_chapters = r"\bhref=['\"](\S+" + \
                re.escape(id_manga.group(0)) + r"\S+)\b"
            links_chapters = re.findall(regex_links_chapters, str(soup))
            links_chapters = list(OrderedDict.fromkeys(links_chapters))

            chapters_return = []
            links_chapters.reverse()
            find_first_manga = False
            for link in links_chapters:
                print(link)
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
        else:
            # print(f'Nenhum resultado encontrado para "{self.name}".')
            return None

    def download_chapters(self):
        chapters_num = self.find_chapters_html()
        for chapter in chapters_num:
            Chapter(self.name, chapter[0], chapter[1],
                    self.path).download_pages()


class Chapter():
    def __init__(self, name, number, link, path):
        self.name = name
        self.number = number
        self.link = link
        self.path = path

    def save_page(self, number_page, bin_image):
        manga_dir = self.path + '\\' + self.name + '\\' + \
            str(self.number) + '\\' + str(number_page) + '.jpg'

        if not os.path.exists(os.path.dirname(manga_dir)):
            try:
                os.makedirs(os.path.dirname(manga_dir))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        with open(manga_dir, 'wb') as image:
            image.write(bin_image)

    def find_pages_html(self):
        b_html = utils.request('', '', self.link)
        if b_html is not None:
            pages = []
            soup = BeautifulSoup(b_html.content, "lxml")
            for tag in soup.find_all('script'):
                pages = re.findall(r"\bsrc='(\w+://\S*)\b", str(tag))
                for page in pages:
                    if ' ' in pages:
                        page = page.replace(' ', '%20')
                if pages:
                    return pages
            print(f'Pages not found')
            return None
        else:
            return None

    def download_pages(self):
        print('-----------------------------------------------')
        print(f'{self.name} - Chapter: {self.number}')
        links_pages = self.find_pages_html()
        index = 1
        if links_pages:
            print('Download started')
            for link in links_pages:
                r = requests.get(link, headers=HEADERS)
                if r.status_code == 404:
                    print('HTTP Error')
                    # break
                self.save_page(index, r.content)
                index += 1
            print('Download completed')
            print(f'Total pages download: {index}')
            print('-----------------------------------------------')
        else:
            print(f'Pages not found')
            print('-----------------------------------------------')


def run_script(name, chapters, path):
    manga = MangaDownload(name)
    MangaRight = Manga(manga.name, manga.link, chapters, path)
    MangaRight.download_chapters()
