import math
import os
from pathlib import Path

import cv2
import numpy as np
import scipy.cluster
import sklearn.cluster
from loguru import logger
from PIL import Image
from sklearn.cluster import KMeans
from cv2 import error as CV2Error
import logger_config

SORTED_DIR = Path.cwd() / 'sorted'
PORRIDGE_DIR = SORTED_DIR / 'porridge'
BROKEN_DIR = SORTED_DIR / 'broken'
COLOR_DIRS = {
    (255, 0, 0): 'red',
    (0, 255, 0): 'green',
    (0, 0, 255): 'blue',
    (0, 0, 0): 'black',
    (255, 255, 255): 'white',
    # (205, 100, 230): 'pink',
    (255, 0, 255): 'purple',
    (255, 255, 0): 'yellow',
    (0, 255, 255): 'bereza',
    (255, 170, 80): 'skin',

}

# создаем папки цветов и переназначаем значения в полный Path
for color, directory in COLOR_DIRS.items():
    color_dir = SORTED_DIR / directory
    COLOR_DIRS[color] = color_dir
    logger.debug(f'Creating color directory for {color}: {color_dir}')
    color_dir.mkdir(parents=True, exist_ok=True)

logger.debug(f'Creating porridge directory: {PORRIDGE_DIR}')
PORRIDGE_DIR.mkdir(parents=True, exist_ok=True)
BROKEN_DIR.mkdir(parents=True, exist_ok=True)


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
    cluster = KMeans(n_clusters=5).fit(reshape)
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

    if len(colors) > 1:
        distance = color_distance(colors[0][1], colors[1][1])
        percentage = (colors[0][0] + colors[1][0]) * 100
    else:
        # logger.critical(list(colors[0]))
        return colors[0][1]


    logger.info(list(colors))
    for perc, color in ((0.7, (255, 255, 255)), (0.7, (0, 0, 0))):
        if closest_color(colors[0][1]) == color:
            if colors[0][0] > perc:
                return color
            else:
                raise PorridgeImageException


    if distance > 200 or percentage < 50:
        logger.info(f'Dominant color was not found')
        logger.info(f'{distance=} {percentage=}')
        logger.info(f'Top-2 colors: {colors[:2]}')
        raise PorridgeImageException

    # if distance > 350 and percentage > 80:
    #     if

    return colors[0][1]


def dominant_imag2(filename):
    import binascii
    import struct

    import numpy as np
    import scipy
    import scipy.cluster
    import scipy.misc
    from PIL import Image

    NUM_CLUSTERS = 5

    # print('reading image')
    im = Image.open(filename)
    im = im.resize((150, 150))      # optional, to reduce time
    ar = np.asarray(im)
    shape = ar.shape
    ar = ar.reshape(scipy.product(shape[:2]), shape[2]).astype(float)

    # print('finding clusters')
    codes, dist = scipy.cluster.vq.kmeans(ar, NUM_CLUSTERS)
    # print('cluster centres:\n', codes)

    vecs, dist = scipy.cluster.vq.vq(ar, codes)         # assign codes
    counts, bins = scipy.histogram(vecs, len(codes))    # count occurrences

    index_max = scipy.argmax(counts)                    # find most frequent
    peak = codes[index_max]
    colour = binascii.hexlify(bytearray(int(c) for c in peak)).decode('ascii')
    # print('most frequent is %s (#%s)' % (peak, colour))
    # print(type(peak), len(peak), list(peak))
    return peak[:-1]


def someons(filename):
    image = Image.open(filename)
    resized = image.resize((5, 5), Image.NEAREST)
    reduced = resized.convert("P", palette=Image.WEB) # convert to web palette (216 colors)
    palette = reduced.getpalette() # get palette as [r,g,b,r,g,b,...]
    palette = [palette[3*n:3*n+3] for n in range(256)] # group 3 by 3 = [[r,g,b],[r,g,b],...]
    color_count = [(n, palette[m]) for n,m in reduced.getcolors()]
    colors = sorted(color_count, key=lambda i: i[0], reverse=True)
    # dominant = colors[0][1]

    distance = color_distance(colors[0][1], colors[1][1])
    percentage = (colors[0][0] + colors[1][0]) * 100

    if distance > 200 or percentage < 50:
        logger.info(f'Dominant color was not found')
        logger.info(f'{distance=} {percentage=}')
        logger.info(f'Top-2 colors: {colors[:2]}')
        raise PorridgeImageException
    return colors[0][1]


def find_dominant_color(filename):
    #Resizing parameters
    width, height = 150,150
    image = Image.open(filename)
    image = image.resize((width, height),resample = 0)
    #Get colors from image object
    pixels = image.getcolors(width * height)
    #Sort them by count number(first element of tuple)
    sorted_pixels = sorted(pixels, key=lambda t: t[0])
    #Get the most frequent color
    dominant_color = sorted_pixels[-1][1]
    return dominant_color[:3]




def dominant_colors(filename):  # PIL image input
    image = Image.open(filename)
    image = image.resize((150, 150))      # optional, to reduce time
    ar = np.asarray(image)
    shape = ar.shape
    ar = ar.reshape(np.product(shape[:2]), shape[2]).astype(float)

    kmeans = sklearn.cluster.MiniBatchKMeans(
        n_clusters=10,
        init="k-means++",
        max_iter=20,
        random_state=1000
    ).fit(ar)
    codes = kmeans.cluster_centers_

    vecs, _dist = scipy.cluster.vq.vq(ar, codes)         # assign codes
    counts, _bins = np.histogram(vecs, len(codes))    # count occurrences

    colors = []
    for index in np.argsort(counts)[::-1]:
        colors.append(tuple([int(code) for code in codes[index]]))
    return colors[0][:3]


def ours(filename):
    image = Image.open(filename)
    resized = image.resize((1, 1), Image.ANTIALIAS)
    return resized.getpixel((0, 0))[:3]


def sort_image(filename):
    try:
        dominant = dominant_image_color(filename)
        closest = closest_color(dominant)
        color_dir = COLOR_DIRS[closest]
        logger.info(f'Dominant color found: {dominant}')
        logger.info(f'Closest color: {closest}')
    except CV2Error:
        logger.info(f'Broken image: {Path(filename)}')
        color_dir = BROKEN_DIR
    except PorridgeImageException:
        color_dir = PORRIDGE_DIR

    logger.info('Sorting into:')
    logger.info(color_dir.name.upper())
    new_filename = color_dir / Path(filename).name
    os.rename(filename, new_filename)
    logger.debug(f'New path: {new_filename}')

