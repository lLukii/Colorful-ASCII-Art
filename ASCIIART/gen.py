from PIL import Image
from numpy import asarray
import os, random

CHARACTER = "@#S%?*+;:,"[::-1]

def rgb_to_ansi(r, g, b) -> int:
    # https://stackoverflow.com/questions/15682537/ansi-color-specific-rgb-sequence-bash
    if r == g and g == b:
        if r < 8:
            return 16
        if r > 248:
            return 231;
        
        return round(((r - 8) / 247) * 24) + 232
    ansi = 16 + (36 * round(r / 255 * 5)) + (6 * round(g / 255 * 5)) + round(b / 255 * 5);
    return ansi

def resize_img(img, w):
    width, height = img.size
    rat = height/(width*1.65)
    h = int(rat*w)
    new_img = img.resize((w, h))
    return new_img

def convert_to_ascii_with_color(img, w):
    data = img.getdata()
    ascii_art = ""
    for i, char in enumerate(data):
        r, g, b = char[0], char[1], char[2]
        avg = (r+g+b)//3
        ascii_art += f"\x1B[38;5;{rgb_to_ansi(r, g, b)}m{CHARACTER[avg//25-1]}" # pls tell me text to rgb actually exists. 
        if (i+1)%w == 0:
            ascii_art += "\n"
    return ascii_art

print("Welcome to ASCII Art!")
print("Created by Lucas Yichen Jiao")
while True:
    try: 
        image_path = input("Please specify the path of your image below: \n")
        f = open(image_path)
        f.close() # initial check for file exsistence. 
    except FileNotFoundError:
        print("Hmmm... the file doesn't seem to exist!")
        continue
    break

size = input("Please specify the size of the image you wish for: (100 is default by pressing ENTER)")
size = 100 if len(size) == 0 else int(size)
try:
    img = resize_img(Image.open(image_path), size)
    data = convert_to_ascii_with_color(img, img.width)

except:
    print("An error occured when trying to process the image!")

print(data)



