from entities import Player, Enemy
from utils import load_image, load_images, Animation
from tilemap import Tilemap
from clouds import Clouds
from spark import Spark
import random, math, sys, pygame, menu
from particle import Particle
class Juego:
    def __init__(self, resolution=None):
        pygame.init()
        if resolution:
            self.current_resolution = resolution
            self.screen = pygame.display.set_mode(self.current_resolution)
        else:
            self.current_resolution = resolution

        self.screen = pygame.display.set_mode(self.current_resolution)
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.mixer.init()
        pygame.display.set_caption("Jump Marius")
        self.screen_display = (640, 480)
        self.current_resolution = self.screen_display
        self.display = pygame.Surface((320, 240), pygame.SRCALPHA)
        self.display_2 = pygame.Surface((320, 240))
        pygame.display.update()
        self.icon = pygame.image.load("recursos/icono.png")
        pygame.display.set_icon(self.icon)
        self.death_count = 0  # Contador de muertes
        self.clock = pygame.time.Clock()
        self.movement = [False, False]

        self.assets = {
            'decor': load_images('tiles/decor'),
            'grass': load_images('tiles/grass'),
            'large_decor': load_images('tiles/large_decor'),
            'stone': load_images('tiles/stone'),
            'player': load_image('entities/player.png'),
            'background': load_image('background.png'),
            'clouds': load_images('clouds'),
            'enemy/idle': Animation(load_images('entities/enemy/idle'), img_dur=6),
            'enemy/run': Animation(load_images('entities/enemy/run'), img_dur=4),
            'player/idle': Animation(load_images('entities/player/idle'), img_dur=6),
            'player/run': Animation(load_images('entities/player/run'), img_dur=4),
            'player/jump': Animation(load_images('entities/player/jump')),
            'player/slide': Animation(load_images('entities/player/slide')),
            'player/wall_slide': Animation(load_images('entities/player/wall_slide')),
            'particle/leaf': Animation(load_images('particles/leaf'), img_dur=20, loop=False),
            'particle/particle': Animation(load_images('particles/particle'), img_dur=6, loop=False),
            'gun': load_image('gun.png'),
            'projectile': load_image('projectile.png'),
            'spawners': load_images('tiles/spawners')
        }
        self.sfx = {
            'jump': pygame.mixer.Sound('recursos/sfx/jump.wav'),
            'dash': pygame.mixer.Sound('recursos/sfx/dash.wav'),
            'hit': pygame.mixer.Sound('recursos/sfx/hit.wav'),
            'shoot': pygame.mixer.Sound('recursos/sfx/shoot.wav'),
            'dead': pygame.mixer.Sound('recursos/sfx/dead.mp3'),
            'ambience': pygame.mixer.Sound('recursos/sfx/ambience.wav'),
            'fondo': pygame.mixer.Sound('recursos/sfx/music.wav')
        }
        
        self.sfx['ambience'].set_volume(0.2)
        self.sfx['shoot'].set_volume(0.4)
        self.sfx['hit'].set_volume(0.8)
        self.sfx['dash'].set_volume(0.3)
        self.sfx['jump'].set_volume(0.7)
        self.sfx['dead'].set_volume(0.3)
        self.sfx['fondo'].set_volume(0.1)
        
        self.clouds = Clouds(self.assets['clouds'], count=16)
        
        self.player = Player(self, (50, 50), (8, 15))
        self.level = 0
        self.tilemap = Tilemap(self, tile_size=16)
        #self.tilemap.load('map.json')
        self.load_level(1)
        self.screenshake = 0
        self.scroll = [0, 0]
    
    def load_level(self, map_id):
        #self.tilemap.load('mapas/map' + str(map_id)    + '.json')
        self.tilemap.load('map.json')
        self.leaf_spawners = []
        for tree in self.tilemap.extract([('large_decor', 2)], keep=True):
            self.leaf_spawners.append(pygame.Rect(4 + tree['pos'][0], 4 + tree['pos'][1], 23, 13))

        self.enemies = []
        for spawner in self.tilemap.extract([('spawners', 0), ('spawners', 1)]):
            if spawner['variant'] == 0:
                self.player.pos = spawner['pos']
                self.player.air_time = 0
            else:
                self.enemies.append(Enemy(self, spawner['pos'], (8, 15)))

        self.projectiles = []
        self.particles = []
        self.sparks = []

        self.scroll = [0, 0]
        self.dead = 0
        self.transition = -30

        
    def reset_game(self):
        # Restablecer todas las variables del juego a su estado inicial
        self.movement = [False, False]

        # Reiniciar el jugador
        self.player.reset_position()
        self.player.reset_state()

        # Reiniciar el mapa de tiles
        self.tilemap = Tilemap(self, tile_size=16)
        self.load_level(1)  # Asegúrate de cargar el nivel nuevamente

        # Reiniciar las nubes
        self.clouds = Clouds(self.assets['clouds'], count=16)

        # Reiniciar el desplazamiento
        self.scroll = [0, 0]


    
    def run(self):
        while True:
            
            menu.main_menu(self.screen, self)  # Ejecutar el menú antes del bucle principal del juego
            while True:               
                self.display.blit(self.assets['background'], (0, 0))
                self.screenshake = max(0, self.screenshake - 1)
            
                if not len(self.enemies):
                    self.transition += 1
                    if self.transition > 30:
                        #self.level = min(self.level + 1, len(os.listdir('data/maps')) - 1)
                        #self.load_level(self.level)
                        pass
                if self.transition < 0:
                    self.transition += 1
                
                if self.dead:
                    self.dead += 1
                    self.death_count += 1
                    game_over_option = menu.game_over_menu(self.screen, self)

                    # Realiza acciones basadas en la opción seleccionada
                    if game_over_option == "restart":
                        self.reset_game()
                    elif game_over_option == "main_menu":
                        return menu.main_menu(self.screen, self)
                    if self.dead >= 10:
                        self.transition = min(30, self.transition + 1)
                    if self.dead > 40:
                        self.load_level(self.level)
                
                self.scroll[0] += (self.player.rect().centerx - self.screen.get_width() / 2 - self.scroll[0]) / 30
                self.scroll[1] += (self.player.rect().centery - self.screen.get_height() / 2 - self.scroll[1]) / 30
                render_scroll = (
                    int((self.player.rect().centerx - self.screen.get_width() / 2)),
                    int((self.player.rect().centery - self.screen.get_height() / 2) )
                )
                for rect in self.leaf_spawners:
                    if random.random() * 49999 < rect.width * rect.height:
                        pos = (rect.x + random.random() * rect.width, rect.y + random.random() * rect.height)
                        self.particles.append(Particle(self, 'leaf', pos, velocity=[-0.1, 0.3], frame=random.randint(0, 20)))
                
                self.clouds.update()
                self.clouds.render(self.display, offset=render_scroll)
                
                self.tilemap.render(self.display, offset=render_scroll)

                for enemy in self.enemies.copy():
                    kill = enemy.update(self.tilemap, (0, 0))
                    enemy.render(self.display, offset=render_scroll)
                    if kill:
                        self.enemies.remove(enemy)
                
                if not self.dead:
                    self.player.update(self.tilemap, ((self.movement[1] - self.movement[0]), 0))
                    self.player.render(self.display, offset=(int(render_scroll[0]), int(render_scroll[1])))

                # [[x, y], direction, timer]
                for projectile in self.projectiles.copy():
                    projectile[0][0] += projectile[1]
                    projectile[2] += 1
                    img = self.assets['projectile']
                    self.display.blit(img, (projectile[0][0] - img.get_width() / 2 - render_scroll[0], projectile[0][1] - img.get_height() / 2 - render_scroll[1]))
                    if self.tilemap.solid_check(projectile[0]):
                        self.projectiles.remove(projectile)
                        for i in range(4):
                            self.sparks.append(Spark(projectile[0], random.random() - 0.5 + (math.pi if projectile[1] > 0 else 0), 2 + random.random()))
                    elif projectile[2] > 360:
                        self.projectiles.remove(projectile)
                        
                    elif abs(self.player.dashing) < 50:
                        if self.player.rect().collidepoint(projectile[0]):
                            self.projectiles.remove(projectile)
                            self.dead += 1
                            self.sfx['hit'].play()
                            self.screenshake = max(16, self.screenshake)
                            for i in range(30):
                                angle = random.random() * math.pi * 2
                                speed = random.random() * 5
                                self.sparks.append(Spark(self.player.rect().center, angle, 2 + random.random()))
                                self.particles.append(Particle(self, 'particle', self.player.rect().center, velocity=[math.cos(angle + math.pi) * speed * 0.5, math.sin(angle + math.pi) * speed * 0.5], frame=random.randint(0, 7)))
                            
                    
                for spark in self.sparks.copy():
                    kill = spark.update()
                    spark.render(self.display, offset=render_scroll)
                    if kill:
                        self.sparks.remove(spark)
                display_mask = pygame.mask.from_surface(self.display)
                display_sillhouette = display_mask.to_surface(setcolor=(0, 0, 0, 180), unsetcolor=(0, 0, 0, 0))
                for offset in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    self.display_2.blit(display_sillhouette, offset)
                
                for particle in self.particles.copy():
                    kill = particle.update()
                    particle.render(self.display, offset=render_scroll)
                    if particle.type == 'leaf':
                        particle.pos[0] += math.sin(particle.animation.frame * 0.035) * 0.3
                    if kill:
                        self.particles.remove(particle)
                
                for enemy in self.enemies.copy():
                    kill_enemy = self.player.check_enemy_collision(enemy)
                    # Ejemplo para ajustar la posición de un enemigo al renderizar
                    enemy.render(self.display, offset=(int(render_scroll[0] ), int(render_scroll[1])))

                    if kill_enemy:
                        self.enemies.remove(enemy)
                
                for particle in self.particles.copy():
                    kill = particle.update()
                    particle.render(self.display, offset=render_scroll)
                    if particle.type == 'leaf':
                        particle.pos[0] += math.sin(particle.animation.frame * 0.035) * 0.3
                    if kill: 
                        self.particles.remove(particle)
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
                            self.sfx['jump'].play()
                        if event.key == pygame.K_x:
                            self.player.dash()
                        elif event.key == pygame.K_ESCAPE:
                            restart_option = menu.restart_menu(self.screen, self)  # Llama a la función del menú de reinicio
                            if restart_option == "restart":
                                self.reset_game()
                                break  # Salir del bucle interno para reiniciar el juego
                            elif restart_option == "main_menu":
                                break  # Salir del bucle interno para volver al menú principal
                    if event.type == pygame.VIDEORESIZE:
                        self.handle_resize_event(event)
                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_LEFT:
                            self.movement[0] = False
                        elif event.key == pygame.K_RIGHT:
                            self.movement[1] = False
                    elif event.type == pygame.VIDEORESIZE:
                        self.handle_resize_event(event)
                if self.transition:
                    transition_surf = pygame.Surface(self.display.get_size())
                    pygame.draw.circle(transition_surf, (255, 255, 255), (self.display.get_width() // 2, self.display.get_height() // 2), (30 - abs(self.transition)) * 8)
                    transition_surf.set_colorkey((255, 255, 255))
                    self.display.blit(transition_surf, (0, 0))
                    
                self.display_2.blit(self.display, (0, 0))
                
                

                screenshake_offset = (random.random() * self.screenshake - self.screenshake / 2, random.random() * self.screenshake - self.screenshake / 2)
                self.screen.blit(pygame.transform.scale(self.display_2, self.screen.get_size()), screenshake_offset)
                scaled_display = pygame.transform.scale(self.display_2, self.current_resolution)
                self.screen.blit(scaled_display, (0, 0))
                pygame.display.update()
                pygame.display.flip()

                self.clock.tick(60)
    def change_resolution(self, resolution):
        self.current_resolution = resolution
        self.screen = pygame.display.set_mode(self.current_resolution)
    def check_enemy_collision(self, enemy):
        player_rect = self.player.rect()
        enemy_rect = enemy.rect()

        # Verifica la colisión con el jugador
        if player_rect.colliderect(enemy_rect):
            if player_rect.right > enemy_rect.left and self.player.last_movement[0] > 0:
                # Colisión por la derecha del jugador
                self.death_count += 1
                self.handle_enemy_collision(enemy)
            elif player_rect.left < enemy_rect.right and self.player.last_movement[0] < 0:
                # Colisión por la izquierda del jugador
                self.death_count += 1
                self.handle_enemy_collision(enemy)
             
            if player_rect.bottom > enemy_rect.top and self.player.last_movement[1] > 0:
                # Colisión por arriba del jugador
                self.death_count += 1
                return self.handle_enemy_collision(enemy)
        return False  # Indica que el enemigo no ha sido eliminado
    
    def change_resolution(self, resolution):
        self.current_resolution = resolution
        self.screen = pygame.display.set_mode(self.current_resolution)
        self.display = pygame.Surface((resolution[0] // 2, resolution[1] // 2), pygame.SRCALPHA)
        self.display_2 = pygame.Surface((resolution[0] // 2, resolution[1] // 2))
        self.clouds = Clouds(self.assets['clouds'], count=16)
        
    def handle_enemy_collision(self, enemy):
        # Acciones a realizar cuando hay colisión con un enemigo
        # Por ejemplo, mostrar el menú de Game Over
        game_over_option = menu.game_over_menu(self.screen, self)

        # Realiza acciones basadas en la opción seleccionada
        if game_over_option == "restart":
            self.reset_game()
        elif game_over_option == "main_menu":
            return menu.main_menu(self.screen, self)
        elif game_over_option == "continue":
            # Elimina al enemigo de la lista de enemigos
            self.enemies.remove(enemy)
            return True  # Indica que el enemigo ha sido eliminado
        
        
