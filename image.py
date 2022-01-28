import random
import string
import requests
from pathlib import Path
from bs4 import BeautifulSoup




IMAGES_DIR = Path.cwd() / 'images'
HTML_DIR = Path.cwd() / 'htmls'


class Downloadable:
    def __init__(self, url):
        self.url = url
        self.path = None



    def download_to(self, path_to_save):
        if self.url.endswith(('jpg', 'png', 'jpeg')):
            mode = 'wb'
            encoding = None
            attr = 'content'
        else:
            mode = 'w'
            encoding = 'utf-8'
            attr = 'text'

        request = requests.get(self.url, headers={'User-Agent': 'Felix'})
        data = getattr(request, attr)

        with open(path_to_save, mode, encoding=encoding) as file:
            file.write(data)
        self.path = path_to_save


class Html(Downloadable):
    def __init__(self, url):
        self.source_url = None
        super().__init__(url)

    def get_source_image_url(self, path_to_save):
        if self.source_url:
            return self.source_url
        if not self.path == path_to_save:
            self.download_to(HTML_DIR)
        with open(path_to_save) as file:
            soup = BeautifulSoup(file, features="html.parser")
        # находим все имг теги
        imgs = soup.find_all('img')

        # из всех имг тегов находим нужный
        for img in imgs:
            if 'class' in img.attrs:
                if img['class'] == ['no-click', 'screenshot-image']:
                    self.source_url = img['src']
                    return self.source_url



class Image:
    def __init__(self):
        self.id = self.generate_id()
        self.hmtl = Html(self.base_url)
        self.source_url = None

    @staticmethod
    def generate_id():
        sequence = string.ascii_lowercase + string.digits
        no_zero_sequence = string.ascii_lowercase + string.digits.replace('0', '')
        # первый символ не может быть нулём
        first_char = random.choice(no_zero_sequence)
        # id от 5 до 6 символов
        image_id = ''.join(random.choice(sequence) for i in range(random.randint(4, 5)))
        return first_char + image_id

    @property
    def unsorted_path(self):
        return Path(IMAGES_DIR) / f'{self.id}.jpg'

    @property
    def html_path(self):
        return Path(HTML_DIR) / f'{self.id}.html'

    @property
    def base_url(self):
        return f'https://prnt.sc/{self.id}'

    def download_source(self, path_to_save):
        if self.source_url is None:
            self.source_url = self.html.get_source_url(self.html_path)
        Downloadable(self.source_url).download_to(path_to_save)
