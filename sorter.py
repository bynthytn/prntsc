import math
import numpy as np
import cv2
import logger_config
import os

from PIL import Image
from sklearn.cluster import KMeans
from loguru import logger
from pathlib import Path


SORTED_DIR = Path.cwd() / 'sorted'
PORRIDGE_DIR = SORTED_DIR / 'porridge'
COLOR_DIRS = {
    (255, 0, 0): 'red',
    (0, 255, 0): 'green',
    (0, 0, 255): 'blue',
    (0, 0, 0): 'black',
    (255, 255, 255): 'white',
    (205, 100, 230): 'pink',
    (110, 42, 137): 'purple',
}

# создаем папки цветов и переназначаем значения в полный Path
for color, directory in COLOR_DIRS.items():
    color_dir = SORTED_DIR / directory
    COLOR_DIRS[color] = color_dir
    logger.debug(f'Creating color directory for {color}: {color_dir}')
    color_dir.mkdir(parents=True, exist_ok=True)

logger.debug(f'Creating porridge directory: {PORRIDGE_DIR}')
PORRIDGE_DIR.mkdir(parents=True, exist_ok=True)

class PorridgeImageException(Exception):
    ...


def closest_color(rgb):
    r, g, b = rgb
    color_diffs = []
    for color in COLOR_DIRS:
        cr, cg, cb = color
        color_diff = math.sqrt((r - cr)**2 + (g - cg)**2 + (b - cb)**2)
        color_diffs.append((color_diff, color))
    return min(color_diffs)[1]


def color_distance(c1, c2):
    (r1,g1,b1) = c1
    (r2,g2,b2) = c2
    return math.sqrt((r1 - r2)**2 + (g1 - g2) ** 2 + (b1 - b2) **2)

# альтернативы:
# https://stackoverflow.com/questions/59507676/how-to-get-the-dominant-colors-using-pillow
# https://stackoverflow.com/questions/29726148/finding-average-color-using-python

def dominant_image_color(filename):
    # https://stackoverflow.com/questions/43111029/how-to-find-the-average-colour-of-an-image-in-python-with-opencv
    image = cv2.imread(str(filename))
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    reshape = image.reshape((image.shape[0] * image.shape[1], 3))

    # Find and display most dominant colors
    cluster = KMeans(n_clusters=4).fit(reshape)
    centroids = cluster.cluster_centers_

    # Get the number of different clusters, create histogram, and normalize
    labels = np.arange(0, len(np.unique(cluster.labels_)) + 1)
    (hist, _) = np.histogram(cluster.labels_, bins = labels)
    hist = hist.astype("float")
    hist /= hist.sum()

    # Create frequency rect and iterate through each cluster's color and percentage
    colors = sorted(
        [(percent, color) for (percent, color) in zip(hist, centroids)],
        reverse=True,
        key=lambda i: i[0]
    )

    distance = color_distance(colors[0][1], colors[1][1])
    percentage = (colors[0][0] + colors[1][0]) * 100

    if distance > 150 or percentage < 50:
        logger.info(f'Dominant color was not found')
        logger.info(f'{distance=} {percentage=}')
        logger.info(f'Top-2 colors: {colors[:2]}')
        raise PorridgeImageException
    return colors[0][1]


def sort_image(filename):
    try:
        dominant = dominant_image_color(filename)
        closest = closest_color(dominant)
        color_dir = COLOR_DIRS[closest]
        logger.info(f'Dominant color found: {dominant}')
        logger.info(f'Closest color: {closest}')
    except PorridgeImageException:
        color_dir = PORRIDGE_DIR

    logger.info('Sorting into:')
    logger.info(color_dir.name.upper())
    new_filename = color_dir / Path(filename).name
    os.rename(filename, new_filename)
    logger.debug(f'New path: {new_filename}')

