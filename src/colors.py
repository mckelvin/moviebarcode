# coding: UTF-8
# ref: http://stackoverflow.com/a/3244061/721331

import sys
import Image
import ImageDraw
import scipy
import scipy.misc
import scipy.cluster

NUM_CLUSTERS = 5

def get_dominant_colors(im, nclusters = NUM_CLUSTERS):
    im = im.resize((150, 150))
    im = im.point(lambda x: x >> 4 << 4) # 256^3 -> 16^3
    ar = scipy.misc.fromimage(im)
    shape = ar.shape
    ar = ar.reshape(scipy.product(shape[:2]), shape[2])
    codes, dist = scipy.cluster.vq.kmeans(ar,nclusters)
    vecs, dist = scipy.cluster.vq.vq(ar, codes)         # assign codes
    counts, bins = scipy.histogram(vecs, len(codes))    # count occurrences
    order = counts.argsort()[::-1]
    sorted_colors = []
    for i in range(len(counts)):
        peak = codes[order[i]]
        sorted_colors.append(tuple(peak[:3]))
    return sorted_colors

def draw_dominant_image(colors,rect_size = (200, 200)):
    img_width = len(colors) * rect_size[0]
    img_height = rect_size[1]
    img = Image.new('RGB',(img_width, img_height))
    draw = ImageDraw.Draw(img)
    for i, color in enumerate(colors):
        draw.rectangle((rect_size[0]*i, 0, rect_size[0]*(i+1), rect_size[1]),fill=color)
    del draw
    return img

def get_dominant_image(im):
    colors = get_dominant_colors(im)
    img = draw_dominant_image(colors)
    return img

if __name__ == '__main__':
    image_path = '/media/Media/Video/[和莎莫的500天].(500).Days.of.Summer.2009.BDRip.480p.x264.AC3-CHD.png'
    im = Image.open(image_path)
    colors = get_dominant_colors(im)
    img = draw_dominant_image(colors)
    img.show()
