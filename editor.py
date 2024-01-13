import sys
import pygame
import tkinter as tk
from tkinter import simpledialog, messagebox

from utils import load_image, load_images
from tilemap import Tilemap

RENDER_SCALE = 2.0

class Editor:
    def __init__(self, map_filename=None):
        pygame.init()

        pygame.display.set_caption('editor')
        self.screen = pygame.display.set_mode((640, 480))
        self.display = pygame.Surface((320, 240))

        self.clock = pygame.time.Clock()

        self.assets = {
            'decor': load_images('tiles/decor'),
            'grass': load_images('tiles/grass'),
            'large_decor': load_images('tiles/large_decor'),
            'stone': load_images('tiles/stone'),
            'spawners': load_images('tiles/spawners'),
            'final': load_images('tiles/final'),
            'hierba': load_images('tiles/newTiles/blocksHierba'),
            'nevados': load_images('tiles/newTiles/blocksNevados'),
            'quemados': load_images('tiles/newTiles/blocksQuemados'),
            'normal': load_images('tiles/newTiles/normalBlocks'),
        }

        self.movement = [False, False, False, False]

        self.tilemap = Tilemap(self, tile_size=16)

        if map_filename:
            try:
                self.tilemap.load(map_filename)
            except FileNotFoundError:
                print(f"El archivo '{map_filename}' no existe. Comenzando con un mapa en blanco.")
        else:
            print("Comenzando con un mapa en blanco.")

        self.scroll = [0, 0]

        self.tile_list = list(self.assets)
        self.tile_group = 0
        self.tile_variant = 0

        self.clicking = False
        self.right_clicking = False
        self.shift = False
        self.ongrid = True

    def show_menu(self):
        root = tk.Tk()
        root.withdraw()
        result = messagebox.askquestion("Menu", "¿Deseas salir sin guardar?", icon='warning')

        if result == 'yes':  # Si selecciona 'Sí', se cierra la aplicación
            pygame.quit()
            sys.exit()
        else:  # Si selecciona 'No', se le pide un nombre y guarda el mapa con ese nombre
            map_name = simpledialog.askstring("Guardar Mapa", "Ingresa el nombre del mapa:")
            if map_name:
                self.tilemap.save(f'mapas/{map_name}.json')

    def run(self):
        while True:
            self.display.fill((0, 0, 0))

            self.scroll[0] += (self.movement[1] - self.movement[0]) * 2
            self.scroll[1] += (self.movement[3] - self.movement[2]) * 2
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            self.tilemap.render(self.display, offset=render_scroll)

            current_tile_images = self.assets[self.tile_list[self.tile_group]][self.tile_variant]
            current_tile_img = current_tile_images.copy()
            current_tile_img.set_alpha(100)

            mpos = pygame.mouse.get_pos()
            mpos = (mpos[0] / RENDER_SCALE, mpos[1] / RENDER_SCALE)
            tile_pos = (
                int((mpos[0] + self.scroll[0]) // self.tilemap.tile_size),
                int((mpos[1] + self.scroll[1]) // self.tilemap.tile_size)
            )

            if self.ongrid:
                self.display.blit(
                    current_tile_img,
                    (tile_pos[0] * self.tilemap.tile_size - self.scroll[0], tile_pos[1] * self.tilemap.tile_size - self.scroll[1])
                )
            else:
                self.display.blit(current_tile_img, mpos)

            if self.clicking and self.ongrid:
                self.tilemap.tilemap[str(tile_pos[0]) + ';' + str(tile_pos[1])] = {
                    'type': self.tile_list[self.tile_group],
                    'variant': self.tile_variant,
                    'pos': tile_pos
                }
            if self.right_clicking:
                tile_loc = str(tile_pos[0]) + ';' + str(tile_pos[1])
                if tile_loc in self.tilemap.tilemap:
                    del self.tilemap.tilemap[tile_loc]
                for tile in self.tilemap.offgrid_tiles.copy():
                    tile_img = self.assets[tile['type']][tile['variant']]
                    tile_r = pygame.Rect(
                        tile['pos'][0] - self.scroll[0],
                        tile['pos'][1] - self.scroll[1],
                        tile_img.get_width(),
                        tile_img.get_height()
                    )
                    if tile_r.collidepoint(mpos):
                        self.tilemap.offgrid_tiles.remove(tile)

            self.display.blit(current_tile_img, (5, 5))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.clicking = True
                        if not self.ongrid:
                            self.tilemap.offgrid_tiles.append({
                                'type': self.tile_list[self.tile_group],
                                'variant': self.tile_variant,
                                'pos': (mpos[0] + self.scroll[0], mpos[1] + self.scroll[1])
                            })
                    if event.button == 3:
                        self.right_clicking = True
                    if self.shift:
                        if event.button == 4:
                            self.tile_variant = (self.tile_variant - 1) % len(self.assets[self.tile_list[self.tile_group]])
                        if event.button == 5:
                            self.tile_variant = (self.tile_variant + 1) % len(self.assets[self.tile_list[self.tile_group]])
                    else:
                        if event.button == 4:
                            self.tile_group = (self.tile_group - 1) % len(self.tile_list)
                            self.tile_variant = 0
                        if event.button == 5:
                            self.tile_group = (self.tile_group + 1) % len(self.tile_list)
                            self.tile_variant = 0
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.clicking = False
                    if event.button == 3:
                        self.right_clicking = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        self.movement[0] = True
                    if event.key == pygame.K_d:
                        self.movement[1] = True
                    if event.key == pygame.K_w:
                        self.movement[2] = True
                    if event.key == pygame.K_s:
                        self.movement[3] = True
                    if event.key == pygame.K_g:
                        self.ongrid = not self.ongrid
                    if event.key == pygame.K_t:
                        self.tilemap.autotile()
                    if event.key == pygame.K_o:
                        self.show_menu()
                    if event.key == pygame.K_ESCAPE:  # Agregado para mostrar el menú al presionar Escape
                        self.show_menu()
                    if event.key == pygame.K_LSHIFT:
                        self.shift = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.movement[0] = False
                    if event.key == pygame.K_d:
                        self.movement[1] = False
                    if event.key == pygame.K_w:
                        self.movement[2] = False
                    if event.key == pygame.K_s:
                        self.movement[3] = False
                    if event.key == pygame.K_LSHIFT:
                        self.shift = False

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    map_filename = simpledialog.askstring("Abrir Mapa", "Ingresa el nombre del mapa a abrir (deja en blanco para comenzar en blanco):")
    Editor(f'mapas/{map_filename}.json').run()
