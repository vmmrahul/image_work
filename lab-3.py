from PIL import Image
import numpy as np

colorset = [
    {'bg' : (255,255,0,255), 'fg' : (50,9,125,255), 'skin': (118,192,0,255)},
    {'bg' : (0,122,240,255), 'fg' : (255,0,112,255), 'skin': (255,255,0,255)},
    {'bg' : (50,0,130,255),'fg' : (255,0,0,255),'skin': (243,145,192,255)},
    {'bg' : (255,126,0,255),'fg' : (134,48,149,255),'skin': (111,185,248,255)},
    {'bg' : (255,0,0,255),'fg' : (35,35,35,255),'skin': (255,255,255,255)},
    {'bg' : (122,192,0,255),'fg' : (255,89,0,255),'skin': (250,255,160,255)},
    {'bg' : (0,114,100,255),'fg' : (252,0,116,255),'skin': (250,250,230,255)},
    {'bg' : (250,255,0,255),'fg' : (254,0,0,255),'skin': (139,198,46,255)},
    {'bg' : (253,0,118,255),'fg' : (51,2,126,255),'skin': (255,105,0,255)}
]


def color_bg_fg(image, bg_color, fg_color):
    '''change transparent background to bg_color and change
    everything non-transparent to fg_color'''
    fg_layer = Image.new('RGBA', image.size, bg_color)
    bg_layer = Image.new('RGBA', image.size, fg_color)
    masked_image = Image.composite(fg_layer, bg_layer, image)
    return masked_image

def white_to_color(image, color):
    '''change all colors close to white and non-transparent
    (alpha > 0) to be color.'''
    threshold=50
    dist=10
    arr=np.array(np.asarray(image))
    r,g,b,a=np.rollaxis(arr,axis=-1)
    mask=((r>threshold)
          & (g>threshold)
          & (b>threshold)
          & (np.abs(r-g)<dist)
          & (np.abs(r-b)<dist)
          & (np.abs(g-b)<dist)
          & (a>0)
          )
    arr[mask]=color
    image=Image.fromarray(arr,mode='RGBA')
    return image

def darken_bg(image, color):
    '''composite image on top of a single-color image, effectively turning all
    transparent parts to that color'''
    color_layer = Image.new('RGBA', image.size, color)
    masked_image = Image.composite(image, color_layer, image)
    return masked_image

def make_warhol_single(image, bg_color, fg_color, skin_color):
    '''create a single warhol-serigraph-style image'''
    bg_fg_layer = color_bg_fg(image, bg_color, fg_color)
    temp_dark_image = darken_bg(image, (0,0,0,255))
    skin_mask = white_to_color(temp_dark_image,(0,0,0,0))
    skin_layer = Image.new('RGBA', image.size, skin_color)
    out = Image.composite(bg_fg_layer, skin_layer, skin_mask)
    return out



def warholify(image_file):
    im = Image.open(image_file).convert('RGBA')

    warhols = []
    for colors in colorset:
        bg = colors['bg']
        fg = colors['fg']
        skin = colors['skin']
        warhols.append(make_warhol_single(im, bg, fg, skin))

    x = im.size[0]
    y = im.size[1]

    blank_image = Image.new("RGB", (x*3, y*3))
    blank_image.paste(warhols[0], (0,0))
    blank_image.paste(warhols[1], (x,0))
    blank_image.paste(warhols[2], (x*2,0))
    blank_image.paste(warhols[3], (0,y))
    blank_image.paste(warhols[4], (x,y))
    blank_image.paste(warhols[5], (x*2,y))
    blank_image.paste(warhols[6], (0,y*2))
    blank_image.paste(warhols[7], (x,y*2))
    blank_image.paste(warhols[8], (x*2,y*2))

    blank_image.save('new_out.png')

warholify('gr.png')

