# -* - coding: UTF-8 -* -
from PIL import Image
import os


# 批量图片压缩处理代码
in_dir = 'C:/Users/Administrator/Desktop/yasuo/'
out_dir = 'C:/Users/Administrator/Desktop/result2/'
filenames = os.listdir(in_dir)


for filename in filenames:
    dir = in_dir+filename+'/'
    if os.path.isdir(dir) == True:
        continue
    for image in os.listdir(dir):
        threshold = 80 * 60
        filesize = os.path.getsize(dir+image)
        if filesize >= threshold:
            with Image.open(dir +image)as im:
                width, height = im.size
                new_width = 600
                new_height = 450
                resized_im = im.resize((new_width, new_height))
                mark = Image.open("C:/Users/Administrator/Desktop/a.jpg")
                layer = Image.new('RGBA', resized_im.size, (0, 0, 0, 0))
                layer.paste(mark, (resized_im.size[0] - 610, resized_im.size[1] - 450))
                out = Image.composite(layer, resized_im, layer)
                output = dir.replace('yasuo', 'result2')
                if os.path.isdir(output) == False:
                    os.mkdir(output)
                out.save(dir.replace('yasuo', 'result2')+image)



