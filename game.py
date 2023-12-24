import pygame
from entities import Player
from utils import load_image, load_images, Animation
import sys
import menu
from tilemap import Tilemap
from clouds import Clouds
class Juego:
    def __init__(self):
        pygame.init()
        
        pygame.display.set_caption("Jump Marius")
        self.screen = pygame.display.set_mode((640, 480))
        self.display = pygame.Surface((320, 240))
        self.icon = pygame.image.load("recursos/icono.png")
        pygame.display.set_icon(self.icon)

        self.clock = pygame.time.Clock()
        self.movement = [False, False]
        
        #self.display = pygame.Surface((320, 240))
        
        self.assets = {
            'decor': load_images('tiles/decor'),
            'grass': load_images('tiles/grass'),
            'large_decor': load_images('tiles/large_decor'),
            'stone': load_images('tiles/stone'),
            'player': load_image('entities/player.png'),
            'background': load_image('background.png'),
            'clouds': load_images('clouds'),
            'player/idle': Animation(load_images('entities/player/idle'), img_dur=6),
            'player/run': Animation(load_images('entities/player/run'), img_dur=4),
            'player/jump': Animation(load_images('entities/player/jump')),
            'player/slide': Animation(load_images('entities/player/slide')),
            'player/wall_slide': Animation(load_images('entities/player/wall_slide')),
        }
        self.clouds = Clouds(self.assets['clouds'], count=16)
        
        self.player = Player(self, (50, 50), (8, 15))
        
        self.tilemap = Tilemap(self, tile_size=16)
        self.tilemap.load('map.json')
        
        self.scroll = [0, 0]
    

    def reset_game(self):
        # Restablecer todas las variables del juego a su estado inicial
        self.movement = [False, False]
        self.player.reset_position()
        #self.tilemap = Tilemap(self, tile_size=16)  
        self.tilemap.load('map.json')
    
    def run(self):
        while True:
            menu.main_menu(self.screen)  # Ejecutar el menú antes del bucle principal del juego
            while True:
                self.display.blit(self.assets['background'], (0, 0))
            
                self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 30
                self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 30
                render_scroll = (int(self.scroll[0]), int(self.scroll[1]))
                
                self.clouds.update()
                self.clouds.render(self.display, offset=render_scroll)
                
                self.tilemap.render(self.display, offset=render_scroll)
                
                self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
                self.player.render(self.display, offset=render_scroll)
            
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT:
                            self.movement[0] = True
                        if event.key == pygame.K_RIGHT:
                            self.movement[1] = True
                        if event.key == pygame.K_UP: # Check if the player is on the ground
                            self.player.jump()  # Call the jump method
                        elif event.key == pygame.K_ESCAPE:
                            restart_option = menu.restart_menu(self.screen)  # Llama a la función del menú de reinicio
                            if restart_option == "restart":
                                self.reset_game()
                                break  # Salir del bucle interno para reiniciar el juego
                            elif restart_option == "main_menu":
                                break  # Salir del bucle interno para volver al menú principal

                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_LEFT:
                            self.movement[0] = False
                        elif event.key == pygame.K_RIGHT:
                            self.movement[1] = False
                self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
                pygame.display.update()
                self.clock.tick(60)

if __name__ == "__main__":
    Juego().run()
