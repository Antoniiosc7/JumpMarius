import pygame
from entities import PhysicsEntity
from utils import load_image
import sys
import menu

class Juego:
    def __init__(self):
        pygame.init()
        
        pygame.display.set_caption("Marius Game")
        self.screen = pygame.display.set_mode((800, 600))
        
        self.icon = pygame.image.load("recursos/icono.png")
        pygame.display.set_icon(self.icon)

        self.clock = pygame.time.Clock()
                
        self.movement = [False, False]
        
        self.assets = {
            'player': pygame.transform.scale(load_image('icono.png')(), (30, 30))
        }
        
        self.player = PhysicsEntity(self, 'player', (50, 50), (8, 15))
        
        self.collision_area = pygame.Rect(50, 50, 300, 50)


    def run(self):
        while True:
            menu.main_menu(self.screen)  # Ejecutar el menú antes del bucle principal del juego
            while True:
                self.screen.fill((14, 219, 248))
                self.player.update((self.movement[1] - self.movement[0], 0))
                self.player.render(self.screen)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT:
                            self.movement[0] = True
                        elif event.key == pygame.K_RIGHT:
                            self.movement[1] = True
                        elif event.key == pygame.K_ESCAPE:
                            menu.main_menu(self.screen)
                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_LEFT:
                            self.movement[0] = False
                        elif event.key == pygame.K_RIGHT:
                            self.movement[1] = False

                self.clock.tick(60)
                pygame.display.update()

if __name__ == "__main__":
    Juego().run()
