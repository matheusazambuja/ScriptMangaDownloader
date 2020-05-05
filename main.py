from manga import Manga

# Domain of sites for downloads:
DOMAIN = {'GOYABU': 'mangayabu.com'}


def main():
    # Domain used for download;
    manga_domain = DOMAIN['GOYABU']
    # Set name manga for download;
    manga_name = 'tower-of-god-season-1'
    # Set chapters to be downloaded;
    manga_chapters = (1, 1)

    # Example directory to store the manga;
    manga_path = r'D:\Files\downloads\mangas'

    manga = Manga(manga_name, manga_chapters, manga_path, manga_domain)
    manga.download_chapters()


if __name__ == '__main__':
    main()
