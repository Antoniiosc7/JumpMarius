import pygame
import os
BASE_IMG_PATH = 'recursos/images/'
BASE_IMG_PATH2 = './recursos/images/'
def load_image(path):
    img = pygame.image.load(BASE_IMG_PATH + path).convert()
    img.set_colorkey((0, 0, 0))
    return img
def load_image1(path):
    img = pygame.image.load('recursos/' + path).convert()
    img.set_colorkey((0, 0, 0))
    return img
def load_images(path):
    images = []
    for img_name in sorted(os.listdir(BASE_IMG_PATH2 + path)):
        images.append(load_image(path + '/' + img_name))
    return images