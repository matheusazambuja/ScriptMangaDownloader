# ScriptMangaDownloader
It's a script/downloader as your name suggests. Created to download mangas from the site mangayabu. Personal use, a utlity for me. Later, updates will be applied to improve its functionality.
## Instalition
1. Install [python] (https://www.python.org) to run the script.
2. Run file dep.bat with double click (just first time run script).
## Use
First edit the file config_download.yaml. It's the manga configuration for download. (name, chapters, domain (mangayabu.com), directory).

Open CMD (Command Prompt) and execute:
```bash
python main.py
```
### Configuration for download in file confi_download:
Note: Standart directory is folder script. (If argument <manga_path> if empty)

Note: Argument <manga_name> exactly like the url of the manga pages (Later updates changed that)
#### Example: manga_name: one-punch-man
Note: Argument <manga_chapters> represent chapters interval. (no spaces between numbers)
#### Example: (1, 3) manga chapters 1 to 3 will be download.
Note: Argument <manga_domain> is site of the download mangas.
