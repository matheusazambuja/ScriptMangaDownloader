from chapter import Chapter


class Manga:
    def __init__(self, name, chapters=(0, 0), path):
        self.name = name
        self.chapters = []
        self._create_chapters(chapters)
        self.path = path.replace('\\', '/')

    def _create_chapters(self, chapters):
        for i in range(chapters[0], chapters[-1]+1):
            if i in range(0, 10):
                self.chapters.append(
                    Chapter(self.name, chr(ord('0')) + str(i)))
            else:
                self.chapters.append(Chapter(self.name, str(i)))

    # def _log_download_chapters(self, function):
    #     def decorator(*args, **kwargs):
    #         print(f'Downaload started:')
    #         function(self)
    #         print(f'Download completed')
    #     return decorator

    def download_chapters(self):
        for chapter in self.chapters:
            chapter.download_pages()
