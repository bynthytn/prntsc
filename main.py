from downloader import download_random_image
from sorter import sort_image
from generator import IMAGES_DIR


for image in IMAGES_DIR.iterdir():
    print(image)
    sort_image(image)


# while True:
#     try:
#         sort_image(download_random_image())
#     except KeyboardInterrupt:
#         exit()
