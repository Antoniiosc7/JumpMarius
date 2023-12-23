import pygame

BASE_IMG_PATH = 'recursos/'

def load_image(path):
    img = pygame.image.load(BASE_IMG_PATH + path).convert
    return img