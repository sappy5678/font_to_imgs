from PIL import ImageFont, ImageDraw, Image, ImageChops
from itertools import chain
from tqdm import tqdm
from fontTools.ttLib import TTFont
from fontTools.unicode import Unicode
import argparse

parser = argparse.ArgumentParser(description='Turn otf to images.')
parser.add_argument('otf', metavar='otf_file', type=str,
                    help='an otf file')
parser.add_argument('--image_folder',  type=str, nargs='?', default="Imgs",
                    help='will put image to this folder.')
parser.add_argument('--image_size',  type=int, nargs='?', default=256,
                    help='image size.')
parser.add_argument('--font_size',  type=int, nargs='?', default=256,
                    help='font size.')

args = parser.parse_args()
opt = vars(args)
print('------------ Options -------------')
for k, v in sorted(opt.items()):
    print('%s: %s' % (str(k), str(v)))
print('-------------- End ----------------')


ttf = TTFont(args.otf, 0, verbose=0, allowVID=0, ignoreDecompileErrors=True, fontNumber=-1)

# Check which word in this font
# 查詢這個字體裡面包含哪些字
chars = chain.from_iterable([y + (Unicode[y[0]],) for y in x.cmap.items()] for x in ttf["cmap"].tables)
char_list = (list(chars))
char_list = tqdm(char_list)

# load font
# 讀取字體
font = ImageFont.truetype(args.otf, args.font_size)

# draw font
# 畫出字體
num = 0
for i in char_list:
    char_unicode = chr(i[0])
    origin = [0, 0]
    txt = Image.new('RGB', (args.image_size, args.image_size), (255, 255, 255))
    draw = ImageDraw.ImageDraw(txt)

    size = draw.textsize(char_unicode,font=font)
    if args.image_size - size[0] < 0:
        origin[0] = args.image_size - size[0]
    else:
        origin[0] = 0
    if args.image_size - size[1] < 0:
        origin[1] = args.image_size - size[1]
    else:
        origin[1] = 0
    # print(size)
    draw.text(tuple(origin), char_unicode, font=font, fill=0)

    # check if the image is whole white
    # 看看圖片是否全白
    if not ImageChops.invert(txt).getbbox():
        continue
    num += 1
    txt.save(args.image_folder + "\\" + str(num) + ".png")
