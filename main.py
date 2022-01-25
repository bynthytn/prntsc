from downloader import download_random_image
from sorter import sort_image

while True:
    try:
        sort_image(download_random_image())
    except KeyboardInterrupt:
        exit()
