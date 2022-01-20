import requests
from bs4 import BeautifulSoup


def get_url_from_html(html_path):

    # открываем файл и парсим супом
    with open(html_path) as file:
        soup = BeautifulSoup(file, features="html.parser")
    # находим все имг теги
    imgs = soup.find_all('img')
    # из всех имг тегов находим нужный
    for img in imgs:
        if 'class' in img.attrs:
            if img['class'] == ['no-click', 'screenshot-image']:
                return img['src']


def download_file(url, path_to_save):
    """ Функция скачивает файл и сохраняет его по заданному пути.
        Принимает в себя два аргумента - url и path_to_save.
        url - ссылка на файл, path_to_save - путь сохранения файла.
        Ежели ссылка оканчивается на jpg, jpeg, png и подобные форматы,
        файл сохранится в качестве байтов (с использованием режима wb)."""

    mode = 'w'
    if url.endswith(('jpg', 'png', 'jpeg')):
        mode += 'b'
        data = requests.get(url, headers={'User-Agent': 'Felix'}).content
        with open(path_to_save, mode) as file:
            file.write(data)
    else:
        data = requests.get(url, headers={'User-Agent': 'Felix'}).text
        with open(path_to_save, mode, encoding="utf-8") as file:
            file.write(data)

"""
html
body
<div class="image-constrain js-image-wrap">
<div class="image-container image__pic js-image-pic">
<img class="no-click screenshot-image"
 """
