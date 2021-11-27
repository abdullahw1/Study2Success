from PIL import Image, ImageDraw, ImageFont
from utils import display_pillow_image

img = Image.new('RGB', (500, 300), color='#FFFFFF')
canvas = ImageDraw.Draw(img)
canvas.text((10, 10), "hello", fill='#000000')