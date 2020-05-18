# ScriptMangaDownloader
It's a script/downloader as your name suggests. Created to download mangas from the site mangahost. Personal use, a utlity for me. Later, updates will be applied to improve its functionality.
## Instalition
1. Install [python] (https://www.python.org) to run the script.
2. Run file dep.bat with double click (just first time run script).
## Use
First edit the file config_download.yaml. It's the manga configuration for download. (name, chapters, directory).

Open CMD (Command Prompt) and execute:
```bash
python main.py
```
### Configuration for download in file config_download:
Note: Standart directory is folder script. (If argument '<manga_path>' is empty)

Note: Argument <manga_chapters> represent chapters interval. (no spaces between numbers)
#### If special or extra chapters within the range, will be downloaded
#### Example: (1,3) chapters 1 to 3 will be download.
#### Example: enter 'all' in <manga_chapters> to download for all chapters manga
