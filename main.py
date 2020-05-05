from manga import Manga


DOMAIN = {'GOYABU': 'mangayabu.com', 'MANGAHOST': 'mangahost.site'}

manga = Manga('tower-of-god-season-1', (17, 17), 'D:\Files\matheus\faculdade\tests\test_downloader')
manga.download_chapters()
