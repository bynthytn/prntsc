import random
import string
from pathlib import Path

IMAGES_DIR = Path.cwd() / 'images'
HTML_DIR = Path.cwd() / 'htmls'
IMAGES_DIR.mkdir(exist_ok=True)
HTML_DIR.mkdir(exist_ok=True)


def generate_id():
    sequence = string.ascii_lowercase + string.digits
    no_zero_sequence = string.ascii_lowercase + string.digits.replace('0', '')
    # первый символ не может быть нулём
    first_char = random.choice(no_zero_sequence)
    # id от 5 до 6 символов
    image_id = ''.join(random.choice(sequence) for i in range(random.randint(4, 5)))
    return first_char + image_id


def generate_image_path(image_id=None):
    if image_id is None:
        image_id = generate_id()
    path = IMAGES_DIR / f'{image_id}.jpg'
    return path


def generate_html_path(image_id=None):
    if image_id is None:
        image_id = generate_id()
    path = HTML_DIR / f'{image_id}.html'
    return path


def generate_html_url(image_id=None):
    base_url = 'https://prnt.sc/'
    if image_id is None:
        image_id = generate_id()
    url = base_url + image_id
    return url
