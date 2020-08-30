import os
import errno
import re
import utils
from bs4 import BeautifulSoup
from collections import OrderedDict


class MangaDownload:
    def __init__(self, name):
        self.name = name
        self.link = ''
        self._select_manga()

    def find_manga_html(self):
        mangas = []
        b_html = utils.request('https://mangahosted.com/find/' + self.name.replace(' ', '+'))
        soup = BeautifulSoup(b_html.content, 'html.parser')
        for tag in soup.find_all('h4', class_='entry-title'):
            tag = tag.find('a')
            tag = str(tag).replace('"', "'")
            name = re.findall(r"(?<=title=')[^']*", str(tag))
            link = re.findall(r"(?<=<a href=')[^']*", str(tag))
            mangas.append({'title': name[0], 'link': link[0]})
        mangas = utils.sort_mangas(mangas, query=self.name)
        return mangas

    def _select_manga(self):
        mangas = self.find_manga_html()
        print(f'Found mangas:')
        for i in range(len(mangas)):
            print(f'{i+1}: {mangas[i]["title"]}')
        print('-----------------------------------------------')
        print('           Enter 0 to end execution')
        print('-----------------------------------------------')
        code_manga = 'a'
        while not code_manga.isdigit() or int(code_manga)-1 not in range(len(mangas)):
            code_manga = input(f'Select a manga: ')
            if code_manga == '0':
                exit(0)
        self.name = mangas[int(code_manga)-1]['title']
        self.link = mangas[int(code_manga)-1]['link']


class Manga:
    def __init__(self, name, link, chapters, path):
        self.name = name
        self.link = link
        self.chapters = chapters
        self.path = path

    def find_chapters_html(self):
        links_chapter = []
        b_html = utils.request(self.link)
        soup = BeautifulSoup(b_html.content, 'html.parser')

        manga_id = re.search(r'mh\d+', b_html.url)
        links_chapter_regex = r"\bhref=['\"](\S+" + re.escape(manga_id.group(0)) + r"\S+)\b"
        links_chapter = re.findall(links_chapter_regex, str(soup))
        links_chapter = list(OrderedDict.fromkeys(links_chapter))

        chapters_return = []
        links_chapter.reverse()
        if self.chapters == (-1, -1):
            first_chapter_find = True
        else:
            first_chapter_find = False
        i = 0
        while True:
            chapter_id_regex = re.escape(manga_id.group(0)) + r'/(\w+(.\w+)?)'
            chapter_id = re.search(chapter_id_regex, links_chapter[i])
            chapter_id = re.sub(re.escape(manga_id.group(0)) + r'/', '', chapter_id.group(0))

            # if chapter_id.isdigit():
            #     if int(chapter_id) in range(self.chapters[0], self.chapters[-1]+1):
            #         chapters_return.append({'id': chapter_id, 'link': links_chapter[i]})
            #     elif int(chapter_id) > self.chapters[-1]:
            #         break

            if chapter_id.isdigit() and chapter_id == str(self.chapters[0]):
                first_chapter_find = True
            if first_chapter_find:
                chapters_return.append({'id': chapter_id, 'link': links_chapter[i]})
                if chapter_id.isdigit() and chapter_id == str(self.chapters[1]):
                    break
            i += 1
        return chapters_return

    def download_chapters(self):
        chapters_num = self.find_chapters_html()
        for chapter in chapters_num:
            print(chapter['id'], chapter['link'])
            Chapter(self.name, chapter['id'], chapter['link'],
                    self.path).download_pages()


class Chapter():
    def __init__(self, name, chapter_id, link, path):
        self.name = name
        self.chapter_id = chapter_id
        self.link = link
        self.path = path

    def save_page(self, number_page, bin_image):
        manga_dir = self.path + '\\' + self.name + '\\' + \
            str(self.chapter_id) + '\\' + str(number_page) + '.webp'

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
        div_slider = BeautifulSoup(b_html.content, 'html.parser').find(name='div', attrs={'id': 'slider'})

        return [tag.img['src'] for tag in div_slider.find_all(name='a')]

    def download_pages(self):
        print('-----------------------------------------------')
        print(f'{self.name} - Chapter: {self.chapter_id}')
        links_pages = self.find_pages_html()
        total_pages_download = 0
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
