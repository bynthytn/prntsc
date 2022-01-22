import random
import string


def generate_id():
    image_id = ''.join(random.choice(string.ascii_lowercase) for i in range(6))
    return image_id


def generate_image_path(image_id=None):
    if image_id is None:
        image_id = generate_id()
    path = f'images\{image_id}.jpg'
    return path


def generate_html_path(image_id=None):
    if image_id is None:
        image_id = generate_id()
    path = f'htmls\{image_id}.html'
    return path


def generate_html_url(image_id=None):
    base_url = 'https://prnt.sc/'
    if image_id is None:
        image_id = generate_id()
    url = base_url + image_id
    return url



