import math

import cv2
import numpy as np
from PIL import Image
from sklearn.cluster import KMeans

SORTED_DIR = 'sorted/'

COLOR_DIRS = {
    (255, 0, 0): 'red/',
    (0, 255, 0): 'green/',
    (0, 0, 255): 'blue/',
    (0, 0, 0): 'black/',
    (255, 255, 255): 'white/',
}


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


def average_image_color(filename):
    # https://stackoverflow.com/questions/29726148/finding-average-color-using-python
    i = Image.open(filename)
    h = i.histogram()

    r = h[0:256]
    g = h[256:256*2]
    b = h[256*2: 256*3]

    # perform the weighted average of each channel:
    # the *index* is the channel value, and the *value* is its weight
    return (
        round(sum( i*w for i, w in enumerate(r) ) / sum(r)),
        round(sum( i*w for i, w in enumerate(g) ) / sum(g)),
        round(sum( i*w for i, w in enumerate(b) ) / sum(b)),
    )


def dominant_image_color(filename):
    # https://stackoverflow.com/questions/59507676/how-to-get-the-dominant-colors-using-pillow
    original = Image.open(filename) # open RGB image
    reduced = original.convert("P", palette=Image.WEB) # convert to web palette (216 colors)
    palette = reduced.getpalette() # get palette as [r,g,b,r,g,b,...]
    palette = [palette[3*n:3*n+3] for n in range(256)] # group 3 by 3 = [[r,g,b],[r,g,b],...]
    color_count = [(n, palette[m]) for n,m in reduced.getcolors()]
    sorted_color_count = sorted(color_count, key=lambda i: i[0], reverse=True)
    # sorted_color_count - лист из туплов
    # (частота_появления_цвета, [р, г, б])
    dominant_color = sorted_color_count[0][1]
    return dominant_color



def color_distance(c1, c2):
    (r1,g1,b1) = c1
    (r2,g2,b2) = c2
    return math.sqrt((r1 - r2)**2 + (g1 - g2) ** 2 + (b1 - b2) **2)


def smart_dominant_color(filename):
    # https://stackoverflow.com/questions/43111029/how-to-find-the-average-colour-of-an-image-in-python-with-opencv
    image = cv2.imread(filename)
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
    colors = sorted([(percent, color) for (percent, color) in zip(hist, centroids)], reverse=True)
    distance = color_distance(colors[0][1], colors[1][1])
    percentage = (colors[0][0] + colors[1][0]) * 100

    if distance > 50 or percentage < 50:
        raise PorridgeImageException

    return colors[0][1]


def sort_image(filename):
    dominant = smart_dominant_color(filename)
    closest = closest_color(dominant)
    print(COLOR_DIRS[closest], dominant, closest)


sort_image('images\pvoczv.jpg')

'''
определить некашную картинку:
если дистанция первых двух доминантных цветов <50
и они вместе >50% картинки
'''


