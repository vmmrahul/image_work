from PIL import Image
import numpy as np

colorset = [
    {'bg': (255, 255, 0, 255), 'fg': (50, 9, 125, 255), 'skin': (118, 192, 0, 255)},
    {'bg': (0, 122, 240, 255), 'fg': (255, 0, 112, 255), 'skin': (255, 255, 0, 255)},
    {'bg': (50, 0, 130, 255), 'fg': (255, 0, 0, 255), 'skin': (243, 145, 192, 255)},
    {'bg': (255, 126, 0, 255), 'fg': (134, 48, 149, 255), 'skin': (111, 185, 248, 255)},
    {'bg': (255, 0, 0, 255), 'fg': (35, 35, 35, 255), 'skin': (255, 255, 255, 255)},
    {'bg': (122, 192, 0, 255), 'fg': (255, 89, 0, 255), 'skin': (250, 255, 160, 255)},
    {'bg': (0, 114, 100, 255), 'fg': (252, 0, 116, 255), 'skin': (250, 250, 230, 255)},
    {'bg': (250, 255, 0, 255), 'fg': (254, 0, 0, 255), 'skin': (139, 198, 46, 255)},
    {'bg': (253, 0, 118, 255), 'fg': (51, 2, 126, 255), 'skin': (255, 105, 0, 255)}
]


def color_bg_fg(image, bg_color, fg_color):
    fg_layer = Image.new('RGBA', image.size, bg_color)
    bg_layer = Image.new('RGBA', image.size, fg_color)
    image = Image.composite(fg_layer, bg_layer, image)
    return image


def add_white_color(image, color):
    arr = np.array(np.asarray(image))
    r, g, b, a = np.rollaxis(arr, axis=-1)
    mask = ((r > 50) & (g > 50) & (b > 50) & (np.abs(r - g) < 10) & (np.abs(r - b) < 10) & (np.abs(g - b) < 10) & (
                a > 0))
    arr[mask] = color
    image = Image.fromarray(arr, mode='RGBA')
    return image


def remain_black(image, color):
    arr = np.array(np.asarray(image))
    r, g, b, a = np.rollaxis(arr, axis=-1)
    mask = ((r != 255) & (g != 255) & (b != 255) & (a != 0))
    arr[mask] = color
    image = Image.fromarray(arr, mode='RGBA')
    return image


def silhouette_image(image, color):
    arr = np.array(np.asarray(image))
    r, g, b, a = np.rollaxis(arr, axis=-1)
    mask = ((r > 130) & (g > 30) & (b > 15))
    arr[mask] = color
    image1 = Image.fromarray(arr, mode='RGBA')
    image = remain_black(image1, (0, 0, 0, 255))
    return image


def remove_greenScreen(image, color):
    arr = np.array(np.asarray(image))
    r, g, b, a = np.rollaxis(arr, axis=-1)
    mask = (g > 235)
    arr[mask] = color
    image = Image.fromarray(arr, mode='RGBA')
    return image


def darken_bg(image, color):
    color_layer = Image.new('RGBA', image.size, color)
    image = Image.composite(image, color_layer, image)
    return image


def make_gr_image(image, bg_color, fg_color, skin_color):
    bg_fg_layer = color_bg_fg(image, bg_color, fg_color)
    temp_dark_image = darken_bg(image, (0, 0, 0, 255))
    skin_mask = add_white_color(temp_dark_image, (0, 0, 0, 0))
    skin_layer = Image.new('RGBA', image.size, skin_color)
    out = Image.composite(bg_fg_layer, skin_layer, skin_mask)
    return out


def main(image_file):
    print("*" * 20, "\nStating")
    print("*" * 20, "\nWork in progress...........")
    im = Image.open(image_file).convert('RGBA')
    r_g = remove_greenScreen(im, (0, 0, 0, 0))
    s_h_image = silhouette_image(r_g, (255, 255, 255, 255))
    s_h_image.save('silhouette_image.png')
    combine = []
    for colors in colorset:
        combine.append(make_gr_image(s_h_image, colors['bg'], colors['fg'], colors['skin']))
    x = im.size[0]
    y = im.size[1]
    new_image = Image.new("RGB", (x * 3, y * 3))
    new_image.paste(combine[0], (0, 0))
    new_image.paste(combine[1], (x, 0))
    new_image.paste(combine[2], (x * 2, 0))
    new_image.paste(combine[3], (0, y))
    new_image.paste(combine[4], (x, y))
    new_image.paste(combine[5], (x * 2, y))
    new_image.paste(combine[6], (0, y * 2))
    new_image.paste(combine[7], (x, y * 2))
    new_image.paste(combine[8], (x * 2, y * 2))
    new_image.save('new_out.png')
    print("*" * 20)
    print("Sucess")


main('gg.png')
