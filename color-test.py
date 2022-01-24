import math

from PIL import Image

original = Image.open(r'images\fiojaz.jpg') # open RGB image
reduced = original.convert("P", palette=Image.WEB) # convert to web palette (216 colors)
palette = reduced.getpalette() # get palette as [r,g,b,r,g,b,...]
palette = [palette[3*n:3*n+3] for n in range(256)] # group 3 by 3 = [[r,g,b],[r,g,b],...]
color_count = [(n, palette[m]) for n,m in reduced.getcolors()]

print(color_count[0])


def average_image_color(filename):

    i = Image.open(filename)
    h = i.histogram()

    # split into red, green, blue
    r = h[0:256]
    g = h[256:256*2]
    b = h[256*2: 256*3]

    # perform the weighted average of each channel:
    # the *index* is the channel value, and the *value* is its weight
    return (
        sum( i*w for i, w in enumerate(r) ) / sum(r),
        sum( i*w for i, w in enumerate(g) ) / sum(g),
        sum( i*w for i, w in enumerate(b) ) / sum(b)
    )

print(average_image_color('images\dheczn.jpg'))


def distance(c1, c2):
    (r1,g1,b1) = c1
    (r2,g2,b2) = c2
    return math.sqrt((r1 - r2)**2 + (g1 - g2) ** 2 + (b1 - b2) **2)

print(distance((179, 228, 228), (115, 198, 206)))


COLORS = (
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
)

def closest_color(rgb):
    # https://stackoverflow.com/questions/54242194/python-find-the-closest-color-to-a-color-from-giving-list-of-colors
    r, g, b = rgb
    color_diffs = []
    for color in COLORS:
        cr, cg, cb = color
        color_diff = math.sqrt((r - cr)**2 + (g - cg)**2 + (b - cb)**2)
        color_diffs.append((color_diff, color))
    return min(color_diffs)[1]

print(closest_color((179, 228, 228)))
