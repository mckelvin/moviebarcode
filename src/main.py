#!/usr/bin/env python2
# coding: UTF-8
#
import os
import sys
import numpy as np
from ffvideo import VideoStream
import Image

from colors import get_dominant_image

BARCODE_SIZE = (1000, 200) # width, height

def get_barcode_image(video_path, barcode_path):
    if os.path.exists(barcode_path):
        return Image.open(barcode_path)
    vs = VideoStream(video_path)
    barcode = Image.new('RGB', BARCODE_SIZE)
    for i, timepoint in enumerate(np.linspace(0, vs.duration, BARCODE_SIZE[0])):
        try:
            frame = vs.get_frame_at_sec(timepoint)
            frame_image = frame.image()
            frame_image = frame_image.resize((1, BARCODE_SIZE[1]), Image.ANTIALIAS)
            barcode.paste(frame_image, (i, 0))
        except Exception, e:
            print e
        finally:
            sys.stdout.write('processing %s [%.2f%%]\r' % (video_path[video_path.rfind(os.path.sep)+1:], timepoint * 100. / vs.duration ))
            sys.stdout.flush()
    barcode.save(barcode_path)
    return barcode

def demo(video_path, barcode_path):
    barcode_image = get_barcode_image(video_path, barcode_path)
    dominant_image = get_dominant_image(barcode_image)
    img_width = max(barcode_image.size[0], dominant_image.size[0])
    img_height = barcode_image.size[1] + dominant_image.size[1]
    img = Image.new('RGB', (img_width, img_height))
    img.paste(barcode_image, (0,0))
    img.paste(dominant_image, (0,barcode_image.size[1]))
    img.show()
    img.save('%s.all.png' % video_path[:video_path.rfind('.')])

def main(argv):
    if len(argv) <= 1:
        print 'Usage: python %s 1.avi [2.mkv 3.wmv ...]' % argv[0]
        return 0

    for video_path in argv[1:]:
        barcode_path = '%s.png' % video_path[:video_path.rfind('.')]
        demo(video_path, barcode_path)

if __name__ == '__main__':
    sys.exit(main(sys.argv))
