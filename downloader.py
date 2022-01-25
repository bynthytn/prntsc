import requests
from bs4 import BeautifulSoup
from loguru import logger

import logger_config
from generator import (generate_html_path, generate_html_url, generate_id,
                       generate_image_path)


def get_src_url_from_html(html_path):

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

    if url.endswith(('jpg', 'png', 'jpeg')):
        mode = 'wb'
        encoding = None
        attr = 'content'
    else:
        mode = 'w'
        encoding = 'utf-8'
        attr = 'text'

    request = requests.get(url, headers={'User-Agent': 'Felix'})
    data = getattr(request, attr)

    with open(path_to_save, mode, encoding=encoding) as file:
        file.write(data)

def download_random_image():
    image_id = generate_id()
    logger.info('___________')
    logger.info(f'Working with: {image_id=}')

    html_path = generate_html_path(image_id)
    image_path = generate_image_path(image_id)
    html_url = generate_html_url(image_id)

    logger.debug(f'Downloading html from {html_url} to {html_path}')
    download_file(html_url, html_path)

    image_url = get_src_url_from_html(html_path)
    logger.debug(f'Got source image url: {image_url}')

    if image_url.startswith('//'):
        logger.error('URL starts with //, probably removed')
        logger.error('Retrying...')
        return download_random_image()

    response = requests.get(image_url, stream=True, headers={'User-Agent': 'Marina'})
    if response.status_code in (403, 520):
        logger.error(f'Status code: {response.status_code}')
        logger.error('Retrying...')
        return download_random_image()

    size_bytes = response.headers['Content-length']
    if size_bytes in ('543', '503'):
        logger.error(f'Image rejected (size is 543 or 503 bytes, probably broken)')
        logger.error('Retrying...')
        return download_random_image()

    logger.debug(f'Downloading image from {image_url} to {image_path}')
    download_file(image_url, image_path)

    return image_path
