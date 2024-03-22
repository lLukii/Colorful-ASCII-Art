import cv2, os
from PIL import Image
from ffpyplayer.player import MediaPlayer
import pygame, sys
import multiprocessing

def resize_frame(img, w) -> Image:
    width, height = img.size
    rat = height/(width*1.65)
    h = int(rat*w)
    new_img = img.resize((w, h))
    return (new_img, h)

CHARACTER = "@#S%?*+;:,"[::-1]
path = input("Enter the path: ")
v_size = input("Enter video size (this will determine the width)")
v_size = 100 if len(v_size) == 0 else int(v_size)
font_size = int(input("Enter Font Size: "))
framerate = float(input("Enter Framerate: "))


video = cv2.VideoCapture(path)
audio = MediaPlayer(path)
pygame.init()
screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
width, height = pygame.display.Info().current_w, pygame.display.Info().current_h
screen = pygame.display.set_mode((width, height))
font = pygame.font.Font("/Users/llukii/Desktop/School/Programming/ASCIIART/OpenSans-Regular.ttf", font_size)
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q: sys.exit()
    
    video.isOpened()
    ret, frame = video.read()
    a_frame, val = audio.get_frame()

    if not ret: break
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image, row_cnt = resize_frame(Image.fromarray(frame), v_size)
    data = image.getdata()
    x, y = 0, 0

    for i, pixel in enumerate(data):
        avg = sum(pixel)//3
        char = CHARACTER[max(int(avg//25-1), 0)]
        txt = font.render(char, True, (pixel[0], pixel[1], pixel[2]))
        center = txt.get_rect(); center.center = (x, y)
        screen.blit(txt, center)
        x += (width-v_size*font_size/2)/(v_size-1) + font_size/2
        if (i+1)%v_size == 0:
            x = 0
            y += (height-row_cnt*font_size/2)/(row_cnt-1) + font_size/2

    if val != 'eof' and a_frame is not None:
        img, t = a_frame
    
    pygame.display.flip()
    screen.fill((0,0,0))
    clock.tick(framerate)


